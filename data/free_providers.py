"""
Base de données des fournisseurs de messagerie gratuits et détection de fautes de frappe (typos).
"""

FREE_PROVIDERS = {
    "gmail.com", "googlemail.com", "yahoo.com", "yahoo.fr", "yahoo.co.uk", "yahoo.es",
    "hotmail.com", "hotmail.fr", "hotmail.co.uk", "hotmail.es", "outlook.com", "outlook.fr",
    "live.com", "live.fr", "msn.com", "icloud.com", "me.com", "mac.com",
    "protonmail.com", "proton.me", "aol.com", "zoho.com", "gmx.com", "gmx.de", "gmx.fr",
    "mail.com", "orange.fr", "wanadoo.fr", "free.fr", "sfr.fr", "laposte.net",
    "web.de", "t-online.de", "freenet.de", "yandex.com", "yandex.ru", "mail.ru"
}

COMMON_TYPOS = {
    "gnail.com": "gmail.com",
    "gmai.com": "gmail.com",
    "gamil.com": "gmail.com",
    "gmial.com": "gmail.com",
    "gmaill.com": "gmail.com",
    "gmail.co": "gmail.com",
    "gmaik.com": "gmail.com",
    "gmaul.com": "gmail.com",
    "hotmial.com": "hotmail.com",
    "hotmaill.com": "hotmail.com",
    "hotmai.com": "hotmail.com",
    "hotmil.com": "hotmail.com",
    "outloo.com": "outlook.com",
    "outlok.com": "outlook.com",
    "outllok.com": "outlook.com",
    "yaho.com": "yahoo.com",
    "yahooo.com": "yahoo.com",
    "protonmai.com": "protonmail.com",
    "iclou.com": "icloud.com",
}

def is_free_provider(domain: str) -> bool:
    return domain.lower().strip() in FREE_PROVIDERS

def check_typo(domain: str) -> str | None:
    return COMMON_TYPOS.get(domain.lower().strip())
