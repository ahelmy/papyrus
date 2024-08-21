from pydantic import BaseModel


class RenderTemplateRequest(BaseModel):
    template_id: str
    data: dict
    format: str
