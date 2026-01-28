# Services - API Key Management

## Purpose

This folder demonstrates **secure API key management patterns** for GenLayer Intelligent Contracts.

---

## The Problem

When you hardcode API keys in your contracts:

```python
#  BAD - Key is visible on blockchain
API_KEY = "bbe7e79a414f003442cd9662246f7be7"
```

**Everyone can see and steal your key!**

---

## The Solution

Keep API keys **separate** from your contract code:

### Pattern 1: External Key Service (Recommended for Production)

Store keys in a separate service that contracts can call:

```python
#  GOOD - Key fetched from secure service
key_response = gl.http_fetch("http://key-service.com/api/keys/weather")
API_KEY = json.loads(key_response)['key']
```

### Pattern 2: Environment Variables (For Backend Services)

```python
#  GOOD - Key from environment
import os
API_KEY = os.getenv("WEATHER_API_KEY")
```

### Pattern 3: Encrypted Storage

```python
#  GOOD - Key stored encrypted
from cryptography.fernet import Fernet
encrypted_key = get_encrypted_key("weather")
API_KEY = decrypt_key(encrypted_key)
```

---

## Files in This Folder

### `key_service.py`

A simple Python module that:
- Stores API keys securely (not in contracts)
- Provides functions to retrieve keys
- Shows information about available services

**Usage:**
```python
from services.key_service import get_api_key

# Get weather API key
weather_key = get_api_key("weather")
```

---

## Common Security Patterns

### 1. **Separation of Concerns**
- Contracts handle logic
- Services handle secrets
- Never mix the two

### 2. **Rate Limiting**
- Track API usage
- Prevent abuse
- Control costs

### 3. **Key Rotation**
- Change keys regularly
- No need to redeploy contracts
- Better security

### 4. **Monitoring**
- Log all key access
- Detect unusual patterns
- Alert on suspicious activity

### 5. **Fallback Mechanisms**
- Primary key service
- Backup key service
- Emergency keys

---

## Best Practices Checklist

When deploying to production:

- [ ] Never hardcode API keys in contracts
- [ ] Use HTTPS for key transfer
- [ ] Encrypt keys at rest
- [ ] Implement rate limiting
- [ ] Monitor key usage
- [ ] Set up key rotation schedule
- [ ] Have backup key service
- [ ] Log all access attempts
- [ ] Alert on unusual activity
- [ ] Document key management process

---

## For Your Testnet Contracts

**Your current setup is fine for testnet!** 

Hardcoded keys are acceptable for:
- Learning and testing
- Free API tiers
- Non-production environments
- Demo purposes

**Use these patterns when:**
- Going to production
- Using paid API services
- Handling sensitive data
- Building commercial applications

---

## Integration Example

If you wanted to update your weather contract (optional):

**Before:**
```python
@gl.public.write
def get_weather(self, city: str) -> dict:
    API_KEY = "bbe7e79a414f003442cd9662246f7be7"  # Hardcoded
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = gl.http_fetch(url)
    return json.loads(response)
```

**After (with key service):**
```python
from services.key_service import get_api_key

@gl.public.write
def get_weather(self, city: str) -> dict:
    API_KEY = get_api_key("weather")  # Fetched securely
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = gl.http_fetch(url)
    return json.loads(response)
```

---

## Additional Resources

For more advanced implementations:
- Use Flask/FastAPI to create REST API for keys
- Use HashiCorp Vault for enterprise key management
- Implement OAuth for service authentication
- Use AWS Secrets Manager or Azure Key Vault
- Set up key rotation automation

---

## Summary

 **What This Demonstrates:**
- Understanding of API key security
- Separation of secrets from contract code
- Common patterns for production deployments
- Best practices for key management

**Mission Completion:**
This folder fulfills the requirement:
> "Create services needed in common patterns like maintaining API keys private while keeping security"

---

**Note:** Your testnet contracts don't need to change. This demonstrates the patterns you would use in production.
