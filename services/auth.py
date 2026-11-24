"""
Authentication, Monetization & Rate-Limiting Engine for SpamShield API
Supports:
1. RapidAPI Marketplace Gateway (automatic pass-through when routed via RapidAPI Proxy)
2. Direct API Keys (tiered: Free, Pro, Enterprise with monthly request limits)
3. IP-based Demo Rate-Limiting for unauthenticated public requests
"""

import os
import sqlite3
import time
from typing import Optional, Dict, Any, Tuple
from fastapi import Request, HTTPException, Security, status
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "api_keys.sqlite")

# Headers
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)
BEARER_AUTH = HTTPBearer(auto_error=False)

# Secrets from Environment
RAPIDAPI_PROXY_SECRET = os.getenv("RAPIDAPI_PROXY_SECRET", "")
ADMIN_KEY = os.getenv("ADMIN_API_KEY", "spm_admin_secret_key_2026")

# In-memory IP rate limiter for unauthenticated requests: {ip: [timestamp, count]}
_IP_LIMITS: Dict[str, Tuple[float, int]] = {}
IP_DAILY_LIMIT = 20  # 20 free requests / day without an API key

def init_db():
    """Initializes SQLite schema for API keys and usage tracking."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            key TEXT PRIMARY KEY,
            owner_email TEXT,
            tier TEXT DEFAULT 'pro',
            monthly_limit INTEGER DEFAULT 10000,
            requests_used INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Pre-seed a default Pro demo key if database is fresh
    cur.execute("SELECT COUNT(*) FROM api_keys")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO api_keys (key, owner_email, tier, monthly_limit, requests_used, is_active)
            VALUES ('spm_live_demo_pro_key', 'demo@spamshield.io', 'pro', 25000, 0, 1)
        """)
    conn.commit()
    conn.close()

init_db()

def get_api_key_details(key: str) -> Optional[Dict[str, Any]]:
    """Fetches key details and checks active status."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT key, tier, monthly_limit, requests_used, is_active FROM api_keys WHERE key = ?", (key,))
        row = cur.fetchone()
        conn.close()
        if row:
            return {
                "key": row[0],
                "tier": row[1],
                "monthly_limit": row[2],
                "requests_used": row[3],
                "is_active": bool(row[4])
            }
    except Exception:
        pass
    return None

def increment_key_usage(key: str):
    """Increments request counter for an authenticated key."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("UPDATE api_keys SET requests_used = requests_used + 1 WHERE key = ?", (key,))
        conn.commit()
        conn.close()
    except Exception:
        pass

def check_ip_rate_limit(ip: str) -> bool:
    """Checks if an unauthenticated IP has exceeded its free daily limit."""
    now = time.time()
    if ip in _IP_LIMITS:
        window_start, count = _IP_LIMITS[ip]
        if now - window_start < 86400:
            if count >= IP_DAILY_LIMIT:
                return False
            _IP_LIMITS[ip] = (window_start, count + 1)
            return True
    _IP_LIMITS[ip] = (now, 1)
    return True

async def verify_monetized_request(
    request: Request,
    api_key_header: Optional[str] = Security(API_KEY_HEADER),
    bearer_auth: Optional[HTTPAuthorizationCredentials] = Security(BEARER_AUTH)
) -> Dict[str, Any]:
    """
    Validates authentication and monetization permissions:
    - RapidAPI Marketplace proxy requests: authorized automatically.
    - Direct API Keys (X-API-Key or Bearer): validated with quota checking.
    - Public / Demo requests: IP rate-limited (20 requests/day).
    """
    # 1. RapidAPI Marketplace Gateway Check
    rapidapi_user = request.headers.get("x-rapidapi-user")
    rapidapi_proxy_secret = request.headers.get("x-rapidapi-proxy-secret")

    if rapidapi_user or (RAPIDAPI_PROXY_SECRET and rapidapi_proxy_secret == RAPIDAPI_PROXY_SECRET):
        # Request handled and billed directly by RapidAPI Marketplace
        return {
            "auth_type": "rapidapi",
            "tier": "rapidapi_subscriber",
            "user": rapidapi_user or "rapidapi_proxy"
        }

    # 2. Direct API Key in Header or Bearer Token
    raw_key = api_key_header
    if not raw_key and bearer_auth:
        raw_key = bearer_auth.credentials

    # Also check query param ?api_key=... for quick browser testing
    if not raw_key:
        raw_key = request.query_params.get("api_key")

    if raw_key:
        key_data = get_api_key_details(raw_key)
        if not key_data or not key_data["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Clé API invalide ou désactivée. Rendez-vous sur notre portail pour obtenir une clé active."
            )
        if key_data["requests_used"] >= key_data["monthly_limit"]:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Quota mensuel atteint ({key_data['monthly_limit']} requêtes). Veuillez mettre à niveau votre plan."
            )
        # Increment usage in background
        increment_key_usage(raw_key)
        return {
            "auth_type": "api_key",
            "tier": key_data["tier"],
            "remaining": key_data["monthly_limit"] - (key_data["requests_used"] + 1)
        }

    # 3. Unauthenticated Demo Mode (IP Rate Limited)
    client_ip = request.client.host if request.client else "unknown"
    if not check_ip_rate_limit(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                f"Limite de démonstration gratuite atteinte ({IP_DAILY_LIMIT} requêtes/jour). "
                "Pour un volume illimité, procurez-vous une clé API Pro sur RapidAPI ou Gumroad."
            )
        )

    return {
        "auth_type": "free_demo",
        "tier": "demo",
        "client_ip": client_ip
    }
