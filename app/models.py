from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Incident(BaseModel):
    id: str
    title: str
    description: str
    severity: int  # 1-5
    status: str  # open, in_progress, resolved, closed
    created_at: datetime
    assigned_to: Optional[str] = None
    tags: List[str] = []

class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: int = 3
    assigned_to: Optional[str] = None
    tags: List[str] = []

class Task(BaseModel):
    id: str
    incident_id: str
    title: str
    done: bool = False
    created_at: datetime

class TaskCreate(BaseModel):
    title: str

