"""In-memory storage for incidents and tasks."""
from typing import Dict, List
from app.models import Incident, Task

incidents: Dict[str, Incident] = {}
tasks: Dict[str, Task] = {}

# NEW: Added for notification tracking
notification_log: List = []
escalation_history: Dict[str, List] = {}

