from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict, Field


class MaintenanceWindowBase(BaseModel):
    start_time: datetime = Field(..., description="Start time of maintenance")
    end_time: datetime = Field(..., description="End time of maintenance")
    message: str = Field(
        default="The system is undergoing scheduled maintenance.",
        description="Message to display to users",
    )
    is_active: bool = Field(default=True, description="Whether the window is active")


class MaintenanceWindowCreate(MaintenanceWindowBase):
    pass


class MaintenanceWindowUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    message: Optional[str] = None
    is_active: Optional[bool] = None


class MaintenanceWindowResponse(MaintenanceWindowBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    created_by: Optional[uuid.UUID] = None
    created_at: datetime
