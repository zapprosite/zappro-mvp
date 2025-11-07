"""Authentication helpers without external dependencies.

Provides password hashing via PBKDF2-HMAC-SHA256 and minimal HS256 JWT
creation/verification using standard library. Intended as a dev-friendly
fallback when installing passlib/jose is not possible. Swap to battle-tested
libs in production.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.user import User

JWT_SECRET = os.getenv("ZAPPRO_JWT_SECRET", "change_me_dev")
JWT_ALG = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ZAPPRO_JWT_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

security = HTTPBearer()


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


def _create_token(
    data: Dict[str, Any], expires_delta: timedelta, token_type: str
) -> str:
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + expires_delta
    to_encode.update(
        {
            "exp": int(exp.timestamp()),
            "type": token_type,
        }
    )
    header = {"alg": JWT_ALG, "typ": "JWT"}
    header_b64 = _b64url(json.dumps(header, separators=",:").encode("utf-8"))
    payload_b64 = _b64url(json.dumps(to_encode, separators=",:").encode("utf-8"))
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = hmac.new(
        JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256
    ).digest()
    return f"{header_b64}.{payload_b64}.{_b64url(signature)}"


def _decode_token(token: str) -> Dict[str, Any]:
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token format")

    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    expected = hmac.new(
        JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256
    ).digest()
    actual = _b64url_decode(signature_b64)
    if not hmac.compare_digest(expected, actual):
        raise HTTPException(status_code=401, detail="Invalid token signature")

    try:
        payload: Dict[str, Any] = json.loads(_b64url_decode(payload_b64))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=401, detail="Invalid token payload") from exc

    exp = int(payload.get("exp", 0))
    if exp and int(datetime.now(timezone.utc).timestamp()) > exp:
        raise HTTPException(status_code=401, detail="Token expired")

    return payload


def create_access_token(data: Dict[str, Any]) -> str:
    return _create_token(
        data,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )


def generate_refresh_token(
    data: Dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    delta = expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return _create_token(data, expires_delta=delta, token_type="refresh")


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    payload = _decode_token(token)
    token_type = payload.get("type")
    if token_type not in (None, "access"):
        raise HTTPException(status_code=401, detail="Invalid token type")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token subject")
    return email


def verify_refresh_token(token: str) -> Dict[str, Any]:
    payload = _decode_token(token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return payload


def get_password_hash(password: str) -> str:
    salt = secrets.token_bytes(16)
    iterations = 200_000
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return "pbkdf2_sha256$%d$%s$%s" % (
        iterations,
        _b64url(salt),
        _b64url(dk),
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        algo, iters_str, salt_b64, hash_b64 = hashed_password.split("$")
        assert algo == "pbkdf2_sha256"
    except Exception:  # noqa: BLE001
        return False
    iterations = int(iters_str)
    salt = _b64url_decode(salt_b64)
    expected = _b64url_decode(hash_b64)
    dk = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(dk, expected)


def get_current_user(
    email: str = Depends(verify_token), db: Session = Depends(get_db)
) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
