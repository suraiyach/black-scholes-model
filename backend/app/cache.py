import json, time
from typing import Any, Optional

try:
    import redis  # type: ignore
except Exception:
    redis = None

class Cache:
    def __init__(self, url: Optional[str], ttl: int = 20):
        self.ttl = ttl
        self.client = None
        if url and redis is not None:
            self.client = redis.from_url(url, decode_responses=True)
        self._mem = {}

    def get(self, key: str) -> Optional[Any]:
        if self.client:
            val = self.client.get(key)
            return json.loads(val) if val else None
        # fallback memory
        entry = self._mem.get(key)
        if not entry:
            return None
        value, expires = entry
        if time.time() > expires:
            self._mem.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any):
        if self.client:
            self.client.setex(key, self.ttl, json.dumps(value))
            return
        self._mem[key] = (value, time.time() + self.ttl)
