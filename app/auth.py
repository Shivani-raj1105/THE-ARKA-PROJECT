import os
import hashlib
import hmac
import base64
import json
import time
from typing import Optional

SECRET_KEY = os.getenv("SECRET_KEY", "organic-botanist-secret-key-change-in-production")


# ── Password hashing (SHA-256 + HMAC, no extra deps) ──────────────────────────

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    key = hmac.new(SECRET_KEY.encode(), salt + password.encode(), hashlib.sha256).digest()
    return base64.b64encode(salt + key).decode()


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        raw = base64.b64decode(stored_hash.encode())
        salt = raw[:16]
        stored_key = raw[16:]
        key = hmac.new(SECRET_KEY.encode(), salt + password.encode(), hashlib.sha256).digest()
        return hmac.compare_digest(key, stored_key)
    except Exception:
        return False


# ── Minimal JWT-like token (base64 JSON + HMAC signature) ─────────────────────

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64url_decode(s: str) -> bytes:
    padding = 4 - len(s) % 4
    return base64.urlsafe_b64decode(s + "=" * padding)


def create_token(user_id: int, email: str, expires_in: int = 86400 * 7) -> str:
    """Create a signed token valid for `expires_in` seconds (default 7 days)."""
    payload = {
        "sub": user_id,
        "email": email,
        "exp": int(time.time()) + expires_in,
    }
    header = _b64url_encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    body = _b64url_encode(json.dumps(payload).encode())
    sig_input = f"{header}.{body}".encode()
    sig = hmac.new(SECRET_KEY.encode(), sig_input, hashlib.sha256).digest()
    return f"{header}.{body}.{_b64url_encode(sig)}"


def decode_token(token: str) -> Optional[dict]:
    """Decode and verify a token. Returns payload dict or None if invalid/expired."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header, body, sig = parts
        sig_input = f"{header}.{body}".encode()
        expected_sig = hmac.new(SECRET_KEY.encode(), sig_input, hashlib.sha256).digest()
        if not hmac.compare_digest(_b64url_decode(sig), expected_sig):
            return None
        payload = json.loads(_b64url_decode(body))
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except Exception:
        return None
