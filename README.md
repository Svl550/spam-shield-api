# SpamShield API — Real-Time Disposable Email & Fraud Detection Cloud API

[![Live API](https://img.shields.io/badge/API%20Status-Live%20Operational-success.svg)](https://spamshield-api-8kdt.onrender.com/health)
[![Documentation](https://img.shields.io/badge/Docs-Swagger%20OpenAPI-blue.svg)](https://spamshield-api-8kdt.onrender.com/docs)
[![Buy Pro Key](https://img.shields.io/badge/Ko--fi-Get%20Pro%20Key-ff5f5f.svg)](https://ko-fi.com/s/fda9dadd03)
[![License](https://img.shields.io/badge/License-Commercial-green.svg)](#)

A high-performance cloud API designed for developers, SaaS platforms, and e-commerce stores to detect and block fake registrations, disposable burner emails, and invalid domains in real time.

---

## ⚡ Live Endpoints

* **Base URL**: `https://spamshield-api-8kdt.onrender.com`
* **Interactive Documentation**: [https://spamshield-api-8kdt.onrender.com/docs](https://spamshield-api-8kdt.onrender.com/docs)
* **OpenAPI Schema**: `https://spamshield-api-8kdt.onrender.com/openapi.json`
* **Get Pro License Key**: **[Instant Access on Ko-fi](https://ko-fi.com/s/fda9dadd03)**

---

## 🔑 Pricing & Commercial License

| Plan | Monthly Requests | Price | Features | Link |
| :--- | :--- | :--- | :--- | :--- |
| **Demo** | 20 / day | Free | Public rate-limited test tier | [Test in Swagger](https://spamshield-api-8kdt.onrender.com/docs) |
| **Pro Key** | Unlimited High-Speed | **$29 Lifetime** | Full commercial rights, sub-10ms latency, priority DNS | **[Buy on Ko-fi](https://ko-fi.com/s/fda9dadd03)** |

---

## 🚀 Quick Code Examples

### cURL
```bash
curl -X GET "https://spamshield-api-8kdt.onrender.com/v1/verify?email=spammer@yopmail.com" \
     -H "X-API-Key: YOUR_PRO_API_KEY"
```

### Python
```python
import requests

url = "https://spamshield-api-8kdt.onrender.com/v1/verify"
headers = {"X-API-Key": "YOUR_PRO_API_KEY"}
params = {"email": "user@gmail.com"}

response = requests.get(url, headers=headers, params=params)
data = response.json()

if data["recommendation"] == "reject":
    print("Blocked disposable/fraudulent registration!")
```

### JavaScript / Node.js
```javascript
const response = await fetch("https://spamshield-api-8kdt.onrender.com/v1/verify?email=user@gmail.com", {
  headers: {
    "X-API-Key": "YOUR_PRO_API_KEY"
  }
});
const result = await response.json();
console.log(result.status, result.risk_score);
```

---

## 🛡️ Response Payload Schema

```json
{
  "email": "spammer@yopmail.com",
  "status": "disposable",
  "syntax_valid": true,
  "is_disposable": true,
  "is_free": false,
  "has_mx": true,
  "mx_records": [
    "smtp.yopmail.com"
  ],
  "did_you_mean": null,
  "risk_score": 99,
  "recommendation": "reject",
  "reasons": [
    "Temporary / Burner email provider detected"
  ]
}
```

---

👉 **Get Your Instant Pro Key**: [https://ko-fi.com/s/fda9dadd03](https://ko-fi.com/s/fda9dadd03)
