"""
End-to-End Monetization & Rate Limiting Tests for SpamShield Micro-SaaS API
"""
import sys
import os
from fastapi.testclient import TestClient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from main import app
from services.auth import ADMIN_KEY

client = TestClient(app)

def run_monetization_tests():
    print("=== Démarrage des tests de monétisation SpamShield ===")
    
    # 1. Test Info & Pricing
    res_pricing = client.get("/v1/pricing")
    assert res_pricing.status_code == 200, f"Erreur pricing: {res_pricing.text}"
    plans = res_pricing.json()["plans"]
    assert len(plans) == 4, f"Nombre de plans incorrect: {len(plans)}"
    print("[PASS] Endpoint /v1/pricing fonctionnel (4 plans tarifaires actifs).")

    # 2. Test Demo Unauthenticated Request
    res_demo = client.get("/v1/verify?email=test@gmail.com")
    assert res_demo.status_code == 200, f"Erreur demo: {res_demo.text}"
    assert res_demo.json()["status"] == "valid"
    print("[PASS] Requête publique / démo autorisée avec succès.")

    # 3. Test Pro API Key Header
    res_pro = client.get("/v1/verify?email=ceo@yopmail.com", headers={"X-API-Key": "spm_live_demo_pro_key"})
    assert res_pro.status_code == 200, f"Erreur Pro key: {res_pro.text}"
    assert res_pro.json()["is_disposable"] is True
    print("[PASS] Authentification par clé API Pro validée.")

    # 4. Test Invalid API Key
    res_invalid = client.get("/v1/verify?email=test@gmail.com", headers={"X-API-Key": "invalid_bad_key_123"})
    assert res_invalid.status_code == 401, f"Échec rejet clé invalide: {res_invalid.status_code}"
    print("[PASS] Rejet immédiat de clé API invalide (401 Unauthorized).")

    # 5. Test RapidAPI Gateway Header
    res_rapidapi = client.get("/v1/verify?email=test@gmail.com", headers={"x-rapidapi-user": "developer_12345"})
    assert res_rapidapi.status_code == 200, f"Erreur RapidAPI proxy: {res_rapidapi.text}"
    print("[PASS] Header RapidAPI proxy transparent et validé.")

    # 6. Test Admin Key Generation
    res_gen = client.post(f"/v1/admin/generate-key?owner_email=newclient@saas.com&tier=ultra&admin_secret={ADMIN_KEY}")
    assert res_gen.status_code == 200, f"Erreur génération admin: {res_gen.text}"
    new_key = res_gen.json()["api_key"]
    assert new_key.startswith("spm_live_"), f"Format de clé incorrect: {new_key}"
    print(f"[PASS] Génération dynamique de clé Ultra : {new_key}")

    # 7. Test Newly Generated Key
    res_new_key = client.get("/v1/verify?email=valid@google.com", headers={"X-API-Key": new_key})
    assert res_new_key.status_code == 200, f"Erreur nouvelle clé: {res_new_key.text}"
    print("[PASS] Nouvelle clé active et opérationnelle immédiatement.")

    print("\n>>> TOUS LES TESTS DE MONÉTISATION SONT VALIDÉS AVEC SUCCÈS ! <<<")

if __name__ == "__main__":
    run_monetization_tests()
