import re
import time
import asyncio
import socket
from typing import Dict, Any, Optional, List

# Essai d'import de dnspython, avec fallback sur socket standard si absent
try:
    import dns.resolver
    import dns.asyncresolver
    HAS_DNSPYTHON = True
except ImportError:
    HAS_DNSPYTHON = False

# Essai d'import de email_validator, avec fallback regex RFC standard si absent
try:
    from email_validator import validate_email as ext_validate_email, EmailNotValidError
    HAS_EMAIL_VALIDATOR = True
except ImportError:
    HAS_EMAIL_VALIDATOR = False

from data.disposable_domains import is_disposable_domain
from data.free_providers import is_free_provider, check_typo

_MX_CACHE: Dict[str, Dict[str, Any]] = {}
CACHE_TTL_SECONDS = 3600

# Regex standard de validation email RFC 5322 simplifiée
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$"
)

async def check_mx_records(domain: str) -> Dict[str, Any]:
    """Vérifie la présence d'enregistrements MX ou A pour le domaine avec cache."""
    domain = domain.lower().strip()
    now = time.time()
    
    if domain in _MX_CACHE:
        cached = _MX_CACHE[domain]
        if now - cached["timestamp"] < CACHE_TTL_SECONDS:
            return cached["data"]

    result = {"has_mx": False, "mx_records": [], "error": None}

    if HAS_DNSPYTHON:
        resolver = dns.asyncresolver.Resolver()
        resolver.timeout = 2.0
        resolver.lifetime = 2.0
        try:
            answers = await resolver.resolve(domain, "MX")
            mx_hosts = [str(r.exchange).rstrip(".") for r in answers]
            result["has_mx"] = len(mx_hosts) > 0
            result["mx_records"] = mx_hosts[:3]
        except Exception as e:
            result["has_mx"] = False
            result["error"] = str(e)
    else:
        # Fallback natif sans dépendance externe via socket DNS
        loop = asyncio.get_event_loop()
        try:
            # Tente de résoudre le domaine (si le domaine existe au niveau DNS)
            await loop.run_in_executor(None, socket.gethostbyname, domain)
            result["has_mx"] = True
            result["mx_records"] = [f"mail.{domain} (inferred via A record)"]
        except Exception as e:
            result["has_mx"] = False
            result["error"] = "Domain resolution failed"

    _MX_CACHE[domain] = {"timestamp": now, "data": result}
    return result

async def verify_email_address(email: str) -> Dict[str, Any]:
    """Analyse complète d'un email."""
    raw_email = (email or "").strip().lower()
    
    if not raw_email or "@" not in raw_email:
        return {
            "email": raw_email,
            "status": "invalid",
            "syntax_valid": False,
            "is_disposable": False,
            "is_free": False,
            "has_mx": False,
            "mx_records": [],
            "did_you_mean": None,
            "risk_score": 100,
            "recommendation": "reject",
            "reasons": ["Invalid email format: missing '@' or empty"]
        }

    # 1. Validation syntaxique
    if HAS_EMAIL_VALIDATOR:
        try:
            val = ext_validate_email(raw_email, check_deliverability=False)
            normalized_email = val.normalized
            local_part = val.local_part
            domain = val.domain
            syntax_valid = True
        except EmailNotValidError as err:
            return {
                "email": raw_email,
                "status": "invalid",
                "syntax_valid": False,
                "is_disposable": False,
                "is_free": False,
                "has_mx": False,
                "mx_records": [],
                "did_you_mean": None,
                "risk_score": 100,
                "recommendation": "reject",
                "reasons": [f"Syntax error: {str(err)}"]
            }
    else:
        if not EMAIL_REGEX.match(raw_email):
            return {
                "email": raw_email,
                "status": "invalid",
                "syntax_valid": False,
                "is_disposable": False,
                "is_free": False,
                "has_mx": False,
                "mx_records": [],
                "did_you_mean": None,
                "risk_score": 100,
                "recommendation": "reject",
                "reasons": ["Syntax error: does not match RFC format"]
            }
        parts = raw_email.split("@", 1)
        local_part = parts[0]
        domain = parts[1]
        normalized_email = raw_email
        syntax_valid = True

    # 2. Détection disposable (jetable)
    is_disposable = is_disposable_domain(domain)
    
    # 3. Détection fournisseur gratuit
    is_free = is_free_provider(domain)
    
    # 4. Détection de typo (faute de frappe)
    suggested_domain = check_typo(domain)
    did_you_mean = f"{local_part}@{suggested_domain}" if suggested_domain else None

    # 5. Vérification DNS MX
    mx_info = await check_mx_records(domain)
    has_mx = mx_info["has_mx"]
    mx_records = mx_info["mx_records"]

    # 6. Calcul du score de risque et statut
    reasons = []

    if is_disposable:
        risk_score = 99
        status = "disposable"
        reasons.append("Temporary / Burner email provider detected")
        recommendation = "reject"
    elif not has_mx:
        risk_score = 90
        status = "undeliverable"
        reasons.append("No active mail server or DNS host found for this domain")
        recommendation = "reject"
    elif suggested_domain:
        risk_score = 75
        status = "typo"
        reasons.append(f"Probable typo in domain, did you mean {suggested_domain}?")
        recommendation = "flag"
    elif is_free:
        risk_score = 15
        status = "valid"
        reasons.append("Valid consumer mailbox (Free webmail)")
        recommendation = "accept"
    else:
        risk_score = 5
        status = "valid"
        reasons.append("Valid business / corporate domain")
        recommendation = "accept"

    return {
        "email": normalized_email,
        "status": status,
        "syntax_valid": syntax_valid,
        "is_disposable": is_disposable,
        "is_free": is_free,
        "has_mx": has_mx,
        "mx_records": mx_records,
        "did_you_mean": did_you_mean,
        "risk_score": risk_score,
        "recommendation": recommendation,
        "reasons": reasons
    }
