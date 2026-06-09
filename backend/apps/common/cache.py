import hashlib
import json
import logging

from django.core.cache import cache

logger = logging.getLogger('gocart')

CACHE_TTL = {
    'products_list': 300,
    'products_featured': 600,
    'categories_tree': 900,
}


def make_cache_key(prefix: str, params: dict | None = None) -> str:
    if not params:
        return prefix
    param_hash = hashlib.md5(
        json.dumps(params, sort_keys=True, default=str).encode()
    ).hexdigest()[:12]
    return f'{prefix}:{param_hash}'


def get_cached(key: str):
    return cache.get(key)


def set_cached(key: str, value, ttl: int = 300):
    cache.set(key, value, ttl)


def invalidate_pattern(prefix: str):
    """Invalidate cache keys by prefix. Requires django-redis."""
    try:
        from django_redis import get_redis_connection
        conn = get_redis_connection('default')
        keys = conn.keys(f'gocart:{prefix}*')
        if keys:
            conn.delete(*keys)
            logger.info(f'Invalidated {len(keys)} cache keys for prefix {prefix}')
    except Exception as e:
        logger.warning(f'Cache invalidation failed: {e}')
