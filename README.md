# API Security Scanner

![Status](https://img.shields.io/badge/status-v0.1%20stable-brightgreen)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Lightweight API security assessment tool. Captures HTTP requests from browser interactions and performs parameter tampering analysis to identify potential security issues.

## 🎯 Features

- **Automated Request Capture** — Intercepts API calls during navigation
- **Parameter Discovery** — Extracts query, header, and JSON body parameters
- **Intelligent Mutation** — Generates contextual test values
- **Response Comparison** — Detects behavioral differences
- **JSON Export** — Complete scan results with reproducibility data
- **Error Resilient** — Continues scanning when requests fail

## 🚀 Quick Start

```bash
# Install
pip install -r requirements.txt

# Run
python main.py
```

1. Enter target URL
2. Navigate the application (browser opens automatically)
3. Let crawler capture API requests (~1 minute)
4. Run security scan
5. Review findings

## 📖 Finding Types

| Type | Indicates |
|------|-----------|
| **Status Code Change** | Parameter affects server logic |
| **Response Content Change** | Behavioral difference detected |
| **Reflected Input** | Possible XSS vector |
| **Server Error** | 5xx response received |

⚠️ **Not all findings are vulnerabilities** — requires manual review.

## ✅ Requirements

- Python 3.8+
- Playwright, Requests, urllib3

See `requirements.txt` for versions.

## 📚 Documentation

- [USAGE_GUIDE.md](USAGE_GUIDE.md) — User guide & troubleshooting
- [SCANNER_README.md](SCANNER_README.md) — Technical reference
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) — Quick start

## ⚖️ Legal Notice

⚠️ Only scan systems you own or have explicit permission to test. Unauthorized security testing is illegal.

Use for:
- ✓ Authorized penetration testing
- ✓ Security research on own systems
- ✓ Educational purposes
- ✓ Bug bounty programs (with permission)

## 📄 License

MIT – see [LICENSE](LICENSE) file

---

**Simple. Reliable. Focused.** v0.1 Stable Release
