from typing import TYPE_CHECKING

from src.core.jinja2 import jinja2_api_env

if TYPE_CHECKING:
    from fastapi import Request


async def render_to_string(template_name: str, context: dict | None = None, request: "Request | None" = None) -> str:
    template = jinja2_api_env.get_template(template_name)

    return await template.render_async(request=request, **context)
