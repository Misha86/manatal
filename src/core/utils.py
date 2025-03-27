from typing import TYPE_CHECKING

from src.config import settings

if TYPE_CHECKING:
    from fastapi import Request


async def render_to_string(template_name: str, context: dict | None = None, request: "Request | None" = None) -> str:
    template = settings.JINJA2_API_ENV.get_template(template_name)

    return await template.render_async(request=request, **context)
