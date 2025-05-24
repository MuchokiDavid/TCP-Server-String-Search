# Production SSL Configuration

## 1. Certificate Requirements
- **Server Certificate**: 
  - SANs covering all domain/IP access points
  - RSA ≥2048-bit or ECDSA P-256
  - Valid TLS Server EKU
- **CA Bundle**:
  - Intermediate certificates chained to trusted root

## 2. Recommended Generation
```bash
# Self-signed for testing (not production!)
openssl req -x509 -newkey rsa:4096 -sha256 -days 365 \
  -nodes -keyout server.key -out server.crt \
  -subj "/CN=string-search.example.com" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"
```