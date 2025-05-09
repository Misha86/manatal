from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.aws.client import s3_client
from src.config import settings
from src.jinja2.cache import RedisBytecodeCache
from src.jinja2.constants import GLOBALS
from src.jinja2.loaders import S3TemplateLoader

bytecode_cache: RedisBytecodeCache = RedisBytecodeCache(
    location=settings.JINJA2_REDIS_CACHE_URL, key_prefix=settings.JINJA2_CACHE_PREFIX, timeout=settings.JINJA2_CACHE_TIMEOUT
)

jinja2_env: Environment = Environment(
    loader=S3TemplateLoader(settings.AWS_S3_BUCKET_NAME, settings.JINJA2_TEMPLATES_FOLDER, s3_client),
    autoescape=select_autoescape(enabled_extensions=("html",)),
    cache_size=settings.JINJA2_CACHE_SIZE,
    bytecode_cache=bytecode_cache,
    trim_blocks=True,
    lstrip_blocks=True,
    enable_async=True,
)

jinja2_env.globals = GLOBALS


if settings.ENVIRONMENT == "local":    
    jinja2_env.loader = FileSystemLoader(settings.JINJA2_TEMPLATES_FOLDER)
