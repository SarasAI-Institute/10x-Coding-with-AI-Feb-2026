from fastapi import FastAPI, HTTPException
from typing import List, Optional
from app.models import Incident, IncidentCreate, Task, TaskCreate
from app.storage import incidents, tasks
from app.utils import (
    gen_id, get_time, sort_incidents, validate_severity, validate_status,
    calculate_incident_stats, format_incident_report, search_incidents
)

app = FastAPI()


@app.get("/incidents")
def get_incidents(status: Optional[str] = None, sort_by: str = "created_at", order: str = "desc"):
    inc_list = list(incidents.values())
    if status:
        inc_list = [i for i in inc_list if i.status == status]
    return sort_incidents(inc_list, sort_by, order)


@app.get("/incidents/search")
def search(q: str):
    return search_incidents(list(incidents.values()), q)


@app.get("/incidents/{incident_id}")
def get_incident(incident_id: str):
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incidents[incident_id]


@app.post("/incidents")
def create_incident(data: IncidentCreate):
    if not validate_severity(data.severity):
        raise HTTPException(status_code=400, detail="Severity must be between 1 and 5")
    inc = Incident(
        id=gen_id(),
        title=data.title,
        description=data.description,
        severity=data.severity,
        status="open",
        created_at=get_time(),
        assigned_to=data.assigned_to,
        tags=data.tags
    )
    incidents[inc.id] = inc
    return inc


@app.put("/incidents/{incident_id}")
def update_incident(incident_id: str, data: IncidentCreate):
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    inc = incidents[incident_id]
    inc.title = data.title
    inc.description = data.description
    inc.severity = data.severity
    inc.assigned_to = data.assigned_to
    inc.tags = data.tags
    return inc


@app.patch("/incidents/{incident_id}/status")
def update_status(incident_id: str, status: str):
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    if not validate_status(status):
        raise HTTPException(status_code=400, detail="Invalid status")
    incidents[incident_id].status = status
    return incidents[incident_id]


@app.patch("/incidents/{incident_id}/assign")
def assign_incident(incident_id: str, assignee: str):
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    incidents[incident_id].assigned_to = assignee
    return incidents[incident_id]


@app.delete("/incidents/{incident_id}")
def delete_incident(incident_id: str):
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    task_ids = [tid for tid, t in tasks.items() if t.incident_id == incident_id]
    for tid in task_ids:
        del tasks[tid]
    del incidents[incident_id]
    return {"deleted": True, "tasks_deleted": len(task_ids)}


@app.get("/incidents/{incident_id}/tasks")
def get_tasks(incident_id: str):
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    return [t for t in tasks.values() if t.incident_id == incident_id]


@app.post("/incidents/{incident_id}/tasks")
def create_task(incident_id: str, data: TaskCreate):
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


@app.patch("/tasks/{task_id}/done")
def mark_done(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id].done = True
    return tasks[task_id]


@app.get("/stats")
def get_stats():
    return calculate_incident_stats(list(incidents.values()))


@app.get("/incidents/{incident_id}/report")
def get_report(incident_id: str):
    if incident_id not in incidents:
        raise HTTPException(status_code=404, detail="Incident not found")
    incident = incidents[incident_id]
    incident_tasks = [t for t in tasks.values() if t.incident_id == incident_id]
    return {"report": format_incident_report(incident, incident_tasks)}

