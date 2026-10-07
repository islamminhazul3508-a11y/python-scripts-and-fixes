import asyncio
import hashlib
import time
from typing import Any, Dict, Optional

class TokenBucketRateLimiter:
    """
    Implements a token bucket algorithm to control asynchronous request rates,
    preventing API rate-limit bans (HTTP 429).
    """
    def __init__(self, rate_per_second: float):
        self.rate = rate_per_second
        self.capacity = rate_per_second
        self.tokens = rate_per_second
        self.last_update = time.monotonic()
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_update = now

            if self.tokens < 1:
                wait_time = (1 - self.tokens) / self.rate
                await asyncio.sleep(wait_time)
                self.tokens = 0
            else:
                self.tokens -= 1

class MemoryCacheManager:
    """
    In-memory TTL (Time-To-Live) cache with cryptographic key hashing
    to prevent redundant computational overhead.
    """
    def __init__(self, default_ttl: int = 60):
        self._store: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl

    def _hash_key(self, key: str) -> str:
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        hashed = self._hash_key(key)
        record = self._store.get(hashed)
        if record:
            if time.time() < record["expiry"]:
                return record["data"]
            del self._store[hashed]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        hashed = self._hash_key(key)
        duration = ttl if ttl is not None else self.default_ttl
        self._store[hashed] = {
            "data": value,
            "expiry": time.time() + duration
        }

class AsyncEngine:
    """
    High-throughput asynchronous execution pipeline combining caching
    and automated rate limiting.
    """
    def __init__(self, requests_per_sec: float = 3.0):
        self.limiter = TokenBucketRateLimiter(requests_per_sec)
        self.cache = MemoryCacheManager(default_ttl=30)

    async def fetch_resource(self, task_id: int, query: str) -> Dict[str, Any]:
        # Step 1: Check Cache
        cached_result = self.cache.get(query)
        if cached_result:
            return {"task_id": task_id, "query": query, "data": cached_result, "source": "CACHE"}

        # Step 2: Rate-limited Network Call Emulation
        await self.limiter.acquire()
        await asyncio.sleep(0.2)  # Simulating async I/O latency
        computed_data = f"Payload_Result_For_{query.upper()}"

        # Step 3: Store in Cache
        self.cache.set(query, computed_data)
        return {"task_id": task_id, "query": query, "data": computed_data, "source": "NETWORK"}

    async def run_pipeline(self, queries: list):
        tasks = [self.fetch_resource(idx, q) for idx, q in enumerate(queries, 1)]
        results = await asyncio.gather(*tasks)
        for res in results:
            print(f"[Task {res['task_id']}] Source: {res['source']} -> Result: {res['data']}")

if __name__ == "__main__":
    # Test asynchronous stream
    sample_queries = ["user_profile", "stock_data", "user_profile", "weather", "stock_data"]
    engine = AsyncEngine(requests_per_sec=2.0)
    asyncio.run(engine.run_pipeline(sample_queries))
