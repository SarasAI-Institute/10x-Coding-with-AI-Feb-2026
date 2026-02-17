"""Pydantic models for the Incident Management API."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Incident(BaseModel):
    """Represents an operational incident."""
    id: str
    title: str
    description: str
    severity: int = Field(ge=1, le=5)
    status: str
    created_at: datetime
    assigned_to: Optional[str] = None
    tags: List[str] = []
    escalation_level: int = 0  # NEW: Added for escalation feature


class IncidentCreate(BaseModel):
    """Schema for creating an incident."""
    title: str
    description: str
    severity: int = Field(default=3, ge=1, le=5)
    assigned_to: Optional[str] = None
    tags: List[str] = []


class Task(BaseModel):
    """Represents a task for an incident."""
    id: str
    incident_id: str
    title: str
    done: bool = False
    created_at: datetime


class TaskCreate(BaseModel):
    """Schema for creating a task."""
    title: str


# NEW: Added by teammate for bulk operations
class BulkIncidentCreate(BaseModel):
    incidents: List[IncidentCreate]


class EscalationRequest(BaseModel):
    reason: str
    notify_emails: List[str] = []

