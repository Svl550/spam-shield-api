from fastapi import FastAPI, Query, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import asyncio
import os
import sqlite3
import time
import uuid

from services.verifier import verify_email_address, _MX_CACHE
from services.auth import verify_monetized_request, DB_PATH, ADMIN_KEY

START_TIME = time.time()

app = FastAPI(
    title="SpamShield - Disposable Email & Fraud Detection API",
    description="""
API haute performance conçue pour les développeurs, SaaS et plateformes e-commerce.
Permet de bloquer en temps réel les faux comptes, emails temporaires (Yopmail, 10MinuteMail, etc.), 
fautes de frappe (typos) et domaines sans serveur MX.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS pour autoriser les requêtes cross-origin si nécessaire
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schémas Pydantic pour documentation Swagger/OpenAPI stricte
class VerificationResponse(BaseModel):
    email: str = Field(..., example="john.doe@gmail.com", description="Email normalisé")
    status: str = Field(..., example="valid", description="Statut : valid, disposable, undeliverable, typo, invalid")
    syntax_valid: bool = Field(..., example=True, description="Conforme à la norme RFC")
    is_disposable: bool = Field(..., example=False, description="Vrai si domaine jetable / temporaire")
    is_free: bool = Field(..., example=True, description="Vrai si fournisseur grand public gratuit (Gmail, Yahoo...)")
    has_mx: bool = Field(..., example=True, description="Vrai si le domaine possède des serveurs mail actifs")
    mx_records: List[str] = Field(default=[], example=["gmail-smtp-in.l.google.com"], description="Liste des hôtes MX")
    did_you_mean: Optional[str] = Field(default=None, example="user@gmail.com", description="Suggestion si faute de frappe détectée")
    risk_score: int = Field(..., example=15, description="Score de risque de 0 (sûr) à 100 (fraude/mort)")
    recommendation: str = Field(..., example="accept", description="Recommandation : accept, flag, reject")
    reasons: List[str] = Field(default=[], description="Détails justifiant la décision")

class BatchVerificationRequest(BaseModel):
    emails: List[str] = Field(..., max_length=100, example=["user1@gmail.com", "fake@yopmail.com", "ceo@company.com"])

class BatchVerificationResponse(BaseModel):
    total: int
    results: List[VerificationResponse]
    processing_time_ms: float

@app.get("/", tags=["Info"])
async def root():
    return {
        "service": "SpamShield API",
        "status": "operational",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", tags=["Info"])
async def health():
    return {
        "status": "healthy",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "cached_domains_count": len(_MX_CACHE)
    }

@app.get("/v1/pricing", tags=["Monetization"])
async def get_pricing_plans():
    """Retourne les formules d'abonnement disponibles pour l'API."""
    return {
        "currency": "USD",
        "plans": [
            {
                "tier": "Basic (Free)",
                "price": 0,
                "monthly_requests": 50,
                "features": ["Single email verification", "Syntax & RFC checks", "MX domain lookup", "Community support"]
            },
            {
                "tier": "Pro",
                "price": 9.99,
                "monthly_requests": 10000,
                "features": ["Single & Batch verification (100/batch)", "Disposable & temporary domain blocking", "Typo auto-correction", "Sub-10ms response time"]
            },
            {
                "tier": "Ultra",
                "price": 29.99,
                "monthly_requests": 50000,
                "features": ["All Pro features", "Priority DNS resolution", "SLA 99.9% uptime", "Commercial license"]
            },
            {
                "tier": "Mega",
                "price": 79.99,
                "monthly_requests": 200000,
                "features": ["All Ultra features", "Dedicated throughput", "Unlimited batch sizes", "Priority integration support"]
            }
        ],
        "rapidapi_marketplace_url": "https://rapidapi.com",
        "direct_purchase_store": "https://ko-fi.com/s/fda9dadd03"
    }

@app.post("/v1/admin/generate-key", tags=["Monetization"])
async def generate_api_key(
    owner_email: str = Query(..., description="Adresse email du client"),
    tier: str = Query("pro", description="Formule: pro, ultra, mega"),
    admin_secret: str = Query(..., description="Clé secrète administrateur")
):
    """Génération sécurisée d'une clé API client (utilisable via webhook de paiement)."""
    if admin_secret != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Clé secrète administrateur incorrecte.")
    
    limits = {"pro": 10000, "ultra": 50000, "mega": 200000}
    limit = limits.get(tier, 10000)
    new_key = f"spm_live_{uuid.uuid4().hex[:16]}"
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO api_keys (key, owner_email, tier, monthly_limit, requests_used, is_active) VALUES (?, ?, ?, ?, 0, 1)",
        (new_key, owner_email, tier, limit)
    )
    conn.commit()
    conn.close()
    
    return {
        "status": "success",
        "api_key": new_key,
        "tier": tier,
        "monthly_limit": limit,
        "owner_email": owner_email
    }

@app.get(
    "/v1/verify",
    response_model=VerificationResponse,
    tags=["Verification"],
    summary="Vérifier une adresse email unique",
    description="Analyse instantanément un email : format, domaine jetable, MX records, et score de risque."
)
async def verify_single_email(
    request: Request,
    email: str = Query(..., description="L'adresse email à analyser", example="support@google.com"),
    auth: Dict[str, Any] = Depends(verify_monetized_request)
):
    if not email:
        raise HTTPException(status_code=400, detail="Le paramètre email est requis.")
    
    result = await verify_email_address(email)
    return result

@app.post(
    "/v1/batch-verify",
    response_model=BatchVerificationResponse,
    tags=["Verification"],
    summary="Vérifier une liste d'adresses emails en masse",
    description="Traite jusqu'à 100 emails simultanément en parallèle avec latence minimale."
)
async def verify_batch_emails(
    payload: BatchVerificationRequest,
    auth: Dict[str, Any] = Depends(verify_monetized_request)
):
    if len(payload.emails) > 100:
        raise HTTPException(status_code=400, detail="La taille maximale d'un batch est de 100 emails.")
        
    start_t = time.perf_counter()
    tasks = [verify_email_address(e) for e in payload.emails]
    results = await asyncio.gather(*tasks)
    elapsed_ms = round((time.perf_counter() - start_t) * 1000, 2)
    
    return {
        "total": len(results),
        "results": results,
        "processing_time_ms": elapsed_ms
    }
