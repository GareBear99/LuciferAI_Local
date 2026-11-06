# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| Latest  | ✅        |

## Reporting a Vulnerability

If you discover a security vulnerability in LuciferAI, please report it responsibly:

1. **Do NOT** open a public GitHub issue for security vulnerabilities.
2. Instead, report via [GitHub Security Advisories](https://github.com/GareBear99/LuciferAI_Local/security/advisories/new).
3. Or contact the maintainer directly through [GitHub](https://github.com/GareBear99).

## What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Response Timeline

- **Acknowledgment**: Within 48 hours
- **Assessment**: Within 1 week
- **Fix**: As soon as possible, depending on severity

## Security Best Practices

LuciferAI is designed with privacy and security as core principles:

- 🔒 **Local-first**: Local inference (Tiers 0-4) sends no model data to the cloud. Note: startup syncs FixNet state from GitHub and runs a WiFi check, so the app is not fully offline on boot; Tier 5 (cloud) is coming soon, not shipped.
- 🛡️ **Fernet Encryption**: FixNet fixes are encrypted (AES-128-CBC + HMAC-SHA256) before sharing
- 🚫 **Fraud Detection**: Blocks dangerous commands (rm -rf, fork bombs, etc.)
- 🔐 **No API Keys Required**: Zero external authentication needed
