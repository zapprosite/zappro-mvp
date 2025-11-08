"""Authentication helpers with async-friendly JWT (RS256) and PBKDF2 hashing."""

from __future__ import annotations

import asyncio
import base64
import binascii
import hashlib
import hmac
import json
import logging
import os
import secrets
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.user import User

LOGGER = logging.getLogger("zappro.auth")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ZAPPRO_JWT_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
TOKEN_ALG = "RS256"
security = HTTPBearer(auto_error=False)


def _normalize_pem(value: str) -> bytes:
    """Convert escaped newlines so keys can be stored as single-line env vars."""

    return value.replace("\\n", "\n").encode("utf-8")


def _read_pem_from_path(path_value: str | None) -> bytes | None:
    if not path_value:
        return None
    try:
        return Path(path_value).expanduser().read_bytes()
    except FileNotFoundError:
        LOGGER.warning("JWT key path %s not found; falling back to dev key", path_value)
    except OSError as exc:  # pragma: no cover - best effort logging
        LOGGER.warning("Unable to read JWT key from %s: %s", path_value, exc)
    return None


def _generate_dev_key_pair() -> tuple[bytes, bytes]:
    LOGGER.warning(
        "ZAPPRO_JWT_PRIVATE_KEY not configured; generating ephemeral RSA key pair "
        "for local development."
    )
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


@lru_cache(maxsize=1)
def _dev_key_pair() -> tuple[bytes, bytes]:
    return _generate_dev_key_pair()


def _load_private_pem() -> bytes:
    env_value = os.getenv("ZAPPRO_JWT_PRIVATE_KEY")
    if env_value:
        return _normalize_pem(env_value)
    file_bytes = _read_pem_from_path(os.getenv("ZAPPRO_JWT_PRIVATE_KEY_PATH"))
    if file_bytes:
        return file_bytes
    return _dev_key_pair()[0]


def _load_public_pem() -> bytes:
    env_value = os.getenv("ZAPPRO_JWT_PUBLIC_KEY")
    if env_value:
        return _normalize_pem(env_value)
    file_bytes = _read_pem_from_path(os.getenv("ZAPPRO_JWT_PUBLIC_KEY_PATH"))
    if file_bytes:
        return file_bytes
    return _dev_key_pair()[1]


@lru_cache(maxsize=1)
def _private_key() -> rsa.RSAPrivateKey:
    return serialization.load_pem_private_key(_load_private_pem(), password=None)


@lru_cache(maxsize=1)
def _public_key() -> rsa.RSAPublicKey:
    return serialization.load_pem_public_key(_load_public_pem())


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


async def _create_token(
    data: Dict[str, Any], expires_delta: timedelta, token_type: str
) -> str:
    payload = data.copy()
    exp = datetime.now(timezone.utc) + expires_delta
    payload.update({"exp": int(exp.timestamp()), "type": token_type})
    header = {"alg": TOKEN_ALG, "typ": "JWT"}
    header_b64 = _b64url(json.dumps(header, separators=",:").encode("utf-8"))
    payload_b64 = _b64url(json.dumps(payload, separators=",:").encode("utf-8"))
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = await asyncio.to_thread(
        _private_key().sign,
        signing_input,
        padding.PKCS1v15(),
        hashes.SHA256(),
    )
    return f"{header_b64}.{payload_b64}.{_b64url(signature)}"


async def _decode_token(token: str) -> Dict[str, Any]:
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    try:
        signature = _b64url_decode(signature_b64)
    except binascii.Error as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc
    try:
        await asyncio.to_thread(
            _public_key().verify,
            signature,
            signing_input,
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
    except InvalidSignature as exc:  # pragma: no cover - deterministic path in tests
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    try:
        payload_bytes = _b64url_decode(payload_b64)
    except binascii.Error as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    try:
        payload: Dict[str, Any] = json.loads(payload_bytes)
    except json.JSONDecodeError as exc:  # noqa: TRY003
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    exp_value = payload.get("exp")
    if exp_value is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        exp_ts = int(exp_value)
    except (TypeError, ValueError) as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    if int(datetime.now(timezone.utc).timestamp()) > exp_ts:
        raise HTTPException(status_code=401, detail="Token expired")

    return payload


async def create_access_token(data: Dict[str, Any]) -> str:
    return await _create_token(
        data,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )


async def generate_refresh_token(
    data: Dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    delta = expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return await _create_token(data, expires_delta=delta, token_type="refresh")


async def verify_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Missing token")

    payload = await _decode_token(credentials.credentials)
    token_type = payload.get("type") or "access"
    if token_type != "access":
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    return str(email)


async def verify_refresh_token(token: str) -> Dict[str, Any]:
    payload = await _decode_token(token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload


async def get_current_user(
    email: str = Depends(verify_token), db: Session = Depends(get_db)
) -> User:
    def _fetch_user() -> User | None:
        return db.query(User).filter(User.email == email).first()

    user = await asyncio.to_thread(_fetch_user)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


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
