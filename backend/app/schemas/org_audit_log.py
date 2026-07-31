import uuid
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any, Union
from datetime import datetime


class OrgAuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Union[uuid.UUID, str]
    organization_id: Union[uuid.UUID, str]
    actor_id: Optional[Union[uuid.UUID, str]] = None
    target_user_id: Optional[Union[uuid.UUID, str]] = None
    action: str
    entity_type: str
    entity_id: Optional[str] = None
    description: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime
    metadata_info: Optional[Dict[str, Any]] = None


class OrgAuditLogPaginatedResponse(BaseModel):
    items: List[OrgAuditLogResponse]
    total: int
    page: int
    limit: int
    pages: int


class CreateOrgAuditLogRequest(BaseModel):
    action: str = Field(..., description="Audit action e.g. member_invited, role_updated, project_created, settings_changed")
    target_user_id: Optional[str] = None
    entity_type: str = "organization"
    entity_id: Optional[str] = None
    description: Optional[str] = None
    metadata_info: Optional[Dict[str, Any]] = None
