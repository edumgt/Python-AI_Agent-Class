from __future__ import annotations

import base64
import hashlib
import hmac
import json
import re
import secrets
import time
from dataclasses import dataclass
from typing import Any

from app.user_store import UserRecord, UserStore

USERNAME_PATTERN = re.compile(r"^[a-z0-9_.-]{3,32}$")
ALLOWED_ORCHESTRATORS = {"native", "langchain", "langgraph"}
ALLOWED_OVERRIDE_KEYS = {
    "openai_model",
    "embedding_provider",
    "openai_embedding_model",
    "stt_model",
    "tts_model",
    "tts_voice",
    "ocr_model",
    "temperature",
    "top_k",
    "use_web_search",
    "web_search_top_k",
    "use_rerank",
    "rerank_provider",
    "langsmith_enabled",
    "orchestrator",
}


@dataclass
class AuthUser:
    user_id: str
    username: str
    full_name: str
    settings: dict[str, Any]
    created_at: str
    updated_at: str


class AuthService:
    def __init__(self, user_store: UserStore, token_secret: str, token_ttl_seconds: int) -> None:
        self._store = user_store
        self._token_secret = token_secret.encode("utf-8")
        self._token_ttl_seconds = max(60, token_ttl_seconds)

    @property
    def backend(self) -> str:
        return getattr(self._store, "backend", "unknown")

    def count_users(self) -> int:
        return self._store.count_users()

    def register(self, username: str, password: str, full_name: str = "") -> tuple[str, AuthUser]:
        key = self._normalize_username(username)
        self._validate_password(password)

        salt = secrets.token_hex(16)
        pw_hash = self._hash_password(password=password, salt=salt)
        created = self._store.create_user(
            username=key,
            password_hash=pw_hash,
            password_salt=salt,
            full_name=full_name,
        )
        token = self._issue_token(user_id=created.user_id, username=created.username)
        return token, self._to_auth_user(created)

    def login(self, username: str, password: str) -> tuple[str, AuthUser]:
        key = self._normalize_username(username)
        user = self._store.get_by_username(key)
        if not user:
            raise ValueError("invalid credentials")
        if not self._verify_password(password=password, salt=user.password_salt, expected_hash=user.password_hash):
            raise ValueError("invalid credentials")
        token = self._issue_token(user_id=user.user_id, username=user.username)
        return token, self._to_auth_user(user)

    def authenticate_token(self, token: str) -> AuthUser:
        payload = self._decode_token(token)
        if int(payload.get("exp", 0)) < int(time.time()):
            raise ValueError("token expired")

        user_id = str(payload.get("sub", "")).strip()
        username = str(payload.get("usr", "")).strip()
        if not user_id or not username:
            raise ValueError("invalid token payload")

        user = self._store.get_by_user_id(user_id)
        if not user or user.username != username:
            raise ValueError("user not found")
        return self._to_auth_user(user)

    def update_settings(self, user_id: str, updates: dict[str, Any]) -> AuthUser:
        clean_updates = self._sanitize_settings_updates(updates)
        updated = self._store.update_settings(user_id=user_id, updates=clean_updates)
        return self._to_auth_user(updated)

    @staticmethod
    def _to_auth_user(user: UserRecord) -> AuthUser:
        return AuthUser(
            user_id=user.user_id,
            username=user.username,
            full_name=user.full_name,
            settings=user.settings,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @staticmethod
    def _normalize_username(username: str) -> str:
        key = username.strip().lower()
        if not USERNAME_PATTERN.match(key):
            raise ValueError("username must match [a-z0-9_.-]{3,32}")
        return key

    @staticmethod
    def _validate_password(password: str) -> None:
        if len(password) < 8:
            raise ValueError("password must be at least 8 characters")
        if not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
            raise ValueError("password must include both letters and numbers")

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200_000)
        return base64.urlsafe_b64encode(dk).decode("utf-8")

    def _verify_password(self, password: str, salt: str, expected_hash: str) -> bool:
        hashed = self._hash_password(password=password, salt=salt)
        return hmac.compare_digest(hashed, expected_hash)

    def _issue_token(self, user_id: str, username: str) -> str:
        payload = {
            "sub": user_id,
            "usr": username,
            "exp": int(time.time()) + self._token_ttl_seconds,
            "iat": int(time.time()),
        }
        body = self._b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
        sig = hmac.new(self._token_secret, body.encode("utf-8"), hashlib.sha256).digest()
        return f"{body}.{self._b64url_encode(sig)}"

    def _decode_token(self, token: str) -> dict[str, Any]:
        try:
            body_b64, sig_b64 = token.split(".", 1)
        except ValueError as exc:
            raise ValueError("invalid token") from exc

        expected_sig = hmac.new(self._token_secret, body_b64.encode("utf-8"), hashlib.sha256).digest()
        actual_sig = self._b64url_decode(sig_b64)
        if not hmac.compare_digest(expected_sig, actual_sig):
            raise ValueError("invalid token signature")

        payload_raw = self._b64url_decode(body_b64)
        try:
            payload = json.loads(payload_raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError("invalid token payload") from exc
        if not isinstance(payload, dict):
            raise ValueError("invalid token payload")
        return payload

    @staticmethod
    def _b64url_encode(raw: bytes) -> str:
        return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")

    @staticmethod
    def _b64url_decode(encoded: str) -> bytes:
        padding = "=" * ((4 - len(encoded) % 4) % 4)
        return base64.urlsafe_b64decode(encoded + padding)

    @staticmethod
    def _sanitize_settings_updates(updates: dict[str, Any]) -> dict[str, Any]:
        clean: dict[str, Any] = {}

        persona_name = updates.get("persona_name")
        if isinstance(persona_name, str):
            name = persona_name.strip()[:64]
            if name:
                clean["persona_name"] = name

        persona_instruction = updates.get("persona_instruction")
        if isinstance(persona_instruction, str):
            clean["persona_instruction"] = persona_instruction.strip()[:1000]

        preferred_orchestrator = updates.get("preferred_orchestrator")
        if isinstance(preferred_orchestrator, str):
            mode = preferred_orchestrator.strip().lower()
            if mode in ALLOWED_ORCHESTRATORS:
                clean["preferred_orchestrator"] = mode

        default_top_k = updates.get("default_top_k")
        if isinstance(default_top_k, int):
            clean["default_top_k"] = max(1, min(20, default_top_k))

        default_use_web_search = updates.get("default_use_web_search")
        if isinstance(default_use_web_search, bool):
            clean["default_use_web_search"] = default_use_web_search

        default_use_rerank = updates.get("default_use_rerank")
        if isinstance(default_use_rerank, bool):
            clean["default_use_rerank"] = default_use_rerank

        enable_langsmith = updates.get("enable_langsmith")
        if isinstance(enable_langsmith, bool):
            clean["enable_langsmith"] = enable_langsmith

        env_overrides = updates.get("env_overrides")
        if isinstance(env_overrides, dict):
            normalized_env: dict[str, Any] = {}
            for key, value in env_overrides.items():
                key_str = str(key).strip().lower()
                if key_str not in ALLOWED_OVERRIDE_KEYS:
                    continue
                if isinstance(value, (str, int, float, bool)):
                    normalized_env[key_str] = value
            clean["env_overrides"] = normalized_env

        return clean
