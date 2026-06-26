import logging

import redis.asyncio as redis
from redis import exceptions as redis_exceptions
from src.config import settings

JTI_EXPIRY = 3600

_redis_client = None
_redis_available = settings.REDIS_ENABLED
_has_warned_redis_unavailable = False
_local_blocklist: set[str] = set()

if settings.REDIS_ENABLED:
    _redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        socket_timeout=1,
        socket_connect_timeout=1,
        retry_on_timeout=True,
    )


def _mark_redis_unavailable(exc: Exception) -> None:
    global _redis_available, _has_warned_redis_unavailable
    _redis_available = False
    if not _has_warned_redis_unavailable:
        logging.warning(f"Redis blocklist unavailable; falling back to in-memory blocklist: {exc}")
        _has_warned_redis_unavailable = True


async def add_jti_to_blocklist(jti: str) -> None:
    if _redis_available and _redis_client is not None:
        try:
            await _redis_client.set(name=jti, value="", ex=JTI_EXPIRY)
            return
        except redis_exceptions.RedisError as exc:
            _mark_redis_unavailable(exc)

    _local_blocklist.add(jti)


async def token_in_blocklist(jti: str) -> bool:
    if _redis_available and _redis_client is not None:
        try:
            jti_value = await _redis_client.get(jti)
            return jti_value is not None
        except redis_exceptions.RedisError as exc:
            _mark_redis_unavailable(exc)

    return jti in _local_blocklist