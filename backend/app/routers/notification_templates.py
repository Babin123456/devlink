from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.notification_template import (
    TemplateInfo,
    TemplateListResponse,
    TemplatePreviewRequest,
    TemplateRenderRequest,
    TemplateRenderResponse,
)
from app.services.notification_template_service import (
    NotificationTemplateService,
    TemplateRenderError,
)

router = APIRouter(tags=["Notification Templates"])

template_service = NotificationTemplateService()


@router.get(
    "/notification-templates",
    response_model=TemplateListResponse,
    summary="List all notification templates",
)
def list_templates():
    templates = []
    for event_type in template_service.list_event_types():
        tmpl = template_service.get_template(event_type)
        if tmpl:
            templates.append(
                TemplateInfo(
                    event_type=tmpl.event_type,
                    title_template=tmpl.title_template,
                    message_template=tmpl.message_template,
                    channels=tmpl.channels,
                )
            )
    return TemplateListResponse(templates=templates)


@router.post(
    "/notification-templates/render",
    response_model=TemplateRenderResponse,
    summary="Render a notification template",
)
def render_template(payload: TemplateRenderRequest):
    result = template_service.render(payload.event_type, payload.variables)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown event type: {payload.event_type}",
        )
    title, message = result
    return TemplateRenderResponse(title=title, message=message)


@router.post(
    "/notification-templates/preview",
    response_model=TemplateRenderResponse,
    summary="Preview a custom template",
)
def preview_template(payload: TemplatePreviewRequest):
    from app.services.notification_template_service import NotificationTemplate

    tmpl = NotificationTemplate(
        event_type="preview",
        title_template=payload.title_template,
        message_template=payload.message_template,
    )
    try:
        title = tmpl.render_title(payload.variables)
        message = tmpl.render_message(payload.variables)
    except TemplateRenderError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return TemplateRenderResponse(title=title, message=message)
