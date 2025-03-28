from pathlib import Path

from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.config import settings
from src.core.cache.backends.redis import RedisBytecodeCache

TEMPLATE_DIRS: list[Path] = [settings.BASE_DIR / "templates"]

bytecode_cache: RedisBytecodeCache = RedisBytecodeCache(
    location=settings.JINJA2_REDIS_URL, key_prefix=settings.JINJA2_CACHE_PREFIX, timeout=settings.JINJA2_CACHE_TIMEOUT
)

jinja2_env: Environment = Environment(
    loader=FileSystemLoader(TEMPLATE_DIRS),
    autoescape=select_autoescape(enabled_extensions=("html",)),
    cache_size=settings.JINJA2_CACHE_SIZE,
    bytecode_cache=bytecode_cache,
    trim_blocks=True,
    lstrip_blocks=True,
    enable_async=True,
)

jinja2_api_env: Jinja2Templates = Jinja2Templates(env=jinja2_env)
