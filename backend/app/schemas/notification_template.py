from __future__ import annotations

from pydantic import BaseModel


class TemplateRenderRequest(BaseModel):
    event_type: str
    variables: dict


class TemplateRenderResponse(BaseModel):
    title: str
    message: str


class TemplateInfo(BaseModel):
    event_type: str
    title_template: str
    message_template: str
    channels: list[str] | None = None


class TemplateListResponse(BaseModel):
    templates: list[TemplateInfo]


class TemplatePreviewRequest(BaseModel):
    title_template: str
    message_template: str
    variables: dict
