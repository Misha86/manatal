import redis
from jinja2.bccache import Bucket, BytecodeCache


class RedisBytecodeCache(BytecodeCache):
    def __init__(self, location: str, key_prefix: str, timeout: int):
        self.client = redis.from_url(location)
        self.prefix = key_prefix
        self.timeout = timeout

    def _key(self, bucket: Bucket):
        """Generate a Redis key for the given bucket."""
        return f"{self.prefix}{bucket.key}"

    def load_bytecode(self, bucket: Bucket):
        """Load compiled template bytecode from Redis."""
        key = self._key(bucket)
        bytecode = self.client.get(key)

        if bytecode:
            bucket.bytecode_from_string(bytecode)

    def dump_bytecode(self, bucket: Bucket):
        """Store compiled template bytecode in Redis."""
        key = self._key(bucket)
        self.client.setex(key, self.timeout, bucket.bytecode_to_string())
