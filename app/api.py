"""FastAPI routes for the Incident Management API."""
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
from typing import List, Optional
from app.models import Incident, IncidentCreate, Task, TaskCreate, BulkIncidentCreate, EscalationRequest
from app.storage import incidents, tasks, notification_log, escalation_history
from app.utils import (
    gen_id, get_time, sort_incidents, validate_severity, validate_status,
    calculate_incident_stats, format_incident_report,
    export_incidents_to_csv, process_bulk_incidents, handle_escalation, send_notification
)

app = FastAPI(
    title="Incident Management API",
    description="API for tracking and managing incidents",
    version="1.0.0"
)


@app.get("/incidents", response_model=List[Incident])
def list_incidents(
    status: Optional[str] = None,
    sort_by: str = "created_at",
    order: str = "desc"
):
    """List all incidents with optional filtering."""
    inc_list = list(incidents.values())
    if status:
        inc_list = [i for i in inc_list if i.status == status]
    return sort_incidents(inc_list, sort_by, order)


@app.get("/incidents/{incident_id}", response_model=Incident)
def get_incident(incident_id: str):
    """Get a single incident by ID."""
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incidents[incident_id]


@app.post("/incidents", response_model=Incident)
def create_incident(data: IncidentCreate):
    """Create a new incident."""
    if not validate_severity(data.severity):
        raise HTTPException(status_code=400, detail="Invalid severity")
    
    inc = Incident(
        id=gen_id(),
        title=data.title,
        description=data.description,
        severity=data.severity,
        status="open",
        created_at=get_time(),
        assigned_to=data.assigned_to,
        tags=data.tags,
        escalation_level=0
    )
    incidents[inc.id] = inc
    return inc


@app.patch("/incidents/{incident_id}/status", response_model=Incident)
def update_status(incident_id: str, status: str = Query(...)):
    """Update incident status."""
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    if not validate_status(status):
        raise HTTPException(status_code=400, detail="Invalid status")
    incidents[incident_id].status = status
    return incidents[incident_id]


@app.delete("/incidents/{incident_id}")
def delete_incident(incident_id: str):
    """Delete an incident and its tasks."""
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    task_ids = [tid for tid, t in tasks.items() if t.incident_id == incident_id]
    for tid in task_ids:
        del tasks[tid]
    del incidents[incident_id]
    return {"deleted": True, "tasks_deleted": len(task_ids)}


@app.get("/incidents/{incident_id}/tasks", response_model=List[Task])
def list_tasks(incident_id: str):
    """List tasks for an incident."""
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    return [t for t in tasks.values() if t.incident_id == incident_id]


@app.post("/incidents/{incident_id}/tasks", response_model=Task)
def create_task(incident_id: str, data: TaskCreate):
    """Create a task for an incident."""
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    t = Task(
        id=gen_id(),
        incident_id=incident_id,
        title=data.title,
        done=False,
        created_at=get_time()
    )
    tasks[t.id] = t
    return t


@app.patch("/tasks/{task_id}/done", response_model=Task)
def mark_task_done(task_id: str):
    """Mark a task as done."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id].done = True
    return tasks[task_id]


@app.get("/stats")
def get_stats():
    """Get incident statistics."""
    return calculate_incident_stats(list(incidents.values()))


# =============================================================================
# NEW ENDPOINTS - Added by teammate, need tests
# =============================================================================

@app.post("/incidents/bulk")
def bulk_create_incidents(data: BulkIncidentCreate):
    """Bulk create multiple incidents at once."""
    result = process_bulk_incidents(
        data.incidents,
        incidents,
        auto_assign=False,
        validate_all=True,
        stop_on_error=False,
        notify=True,
        notification_list=notification_log
    )
    return result


@app.get("/incidents/export", response_class=PlainTextResponse)
def export_incidents():
    """Export all incidents as CSV."""
    csv_content = export_incidents_to_csv(
        list(incidents.values()),
        include_tasks=True,
        tasks_dict=tasks
    )
    return csv_content


@app.post("/incidents/{incident_id}/escalate")
def escalate_incident(incident_id: str, data: EscalationRequest):
    """Escalate an incident to higher priority."""
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    result = handle_escalation(
        incidents[incident_id],
        data,
        escalation_history,
        notification_log,
        max_level=3,
        update_severity=True
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.get("/incidents/{incident_id}/escalation-history")
def get_escalation_history(incident_id: str):
    """Get escalation history for an incident."""
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    return escalation_history.get(incident_id, [])


@app.post("/incidents/{incident_id}/notify")
def notify_about_incident(
    incident_id: str,
    emails: List[str] = Query(...),
    message: Optional[str] = None
):
    """Send notification about an incident."""
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    result = send_notification(
        "manual",
        incident_id,
        emails,
        message=message,
        log_list=notification_log,
        include_incident_details=True,
        incident_dict=incidents
    )
    return result

