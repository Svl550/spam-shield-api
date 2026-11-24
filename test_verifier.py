import asyncio
from services.verifier import verify_email_address

async def run_tests():
    test_cases = [
        ("spammer@yopmail.com", "disposable", 99, "reject"),
        ("fakeuser@temp-mail.org", "disposable", 99, "reject"),
        ("typo_user@gnail.com", "typo", 75, "flag"),
        ("not_an_email", "invalid", 100, "reject"),
        ("valid_user@gmail.com", "valid", 15, "accept"),
    ]
    
    print("=== Démarrage des tests unitaires ===")
    all_passed = True
    for email, expected_status, expected_min_score, expected_rec in test_cases:
        res = await verify_email_address(email)
        status_ok = res["status"] == expected_status
        score_ok = res["risk_score"] >= expected_min_score if expected_min_score > 50 else res["risk_score"] <= 30
        rec_ok = res["recommendation"] == expected_rec
        
        passed = status_ok and score_ok and rec_ok
        print(f"[{'PASS' if passed else 'FAIL'}] {email} -> status={res['status']}, score={res['risk_score']}, rec={res['recommendation']}")
        if not passed:
            all_passed = False
            
    if all_passed:
        print(">>> TOUS LES TESTS SONT VALIDES ! <<<")
    else:
        print(">>> CERTAINS TESTS ONT ÉCHOUÉ <<<")

if __name__ == "__main__":
    asyncio.run(run_tests())
