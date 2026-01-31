from fastapi import FastAPI, HTTPException
from typing import List, Optional
from app.models import Incident, IncidentCreate, Task, TaskCreate
from app.storage import incidents, tasks
from app.utils import gen_id, get_time, sort_incidents, validate_severity

app = FastAPI()

# get all incidents
@app.get("/incidents")
def get_incidents(status: Optional[str] = None, sort_by: str = "created_at"):
    inc_list = list(incidents.values())
    if status:
        inc_list = [i for i in inc_list if i.status == status]
    return sort_incidents(inc_list, sort_by, "desc")

@app.get("/incidents/{incident_id}")
def get_incident(incident_id: str):
    # TODO: finish this endpoint
    raise NotImplementedError()

@app.post("/incidents")
def create_incident(data: IncidentCreate):
    if not validate_severity(data.severity):
        raise HTTPException(status_code=400, detail="invalid severity")
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
        raise HTTPException(status_code=404)
    inc = incidents[incident_id]
    inc.title = data.title
    inc.description = data.description
    inc.severity = data.severity
    inc.assigned_to = data.assigned_to
    inc.tags = data.tags
    return inc

@app.patch("/incidents/{incident_id}/status")
def update_status(incident_id: str, status: str):
    # BUG: doesn't validate status value
    if incident_id not in incidents:
        raise HTTPException(status_code=404)
    incidents[incident_id].status = status
    return incidents[incident_id]

@app.delete("/incidents/{incident_id}")
def delete_incident(incident_id: str):
    if incident_id not in incidents:
        raise HTTPException(status_code=404)
    # delete related tasks too
    del incidents[incident_id]
    # BUG: forgets to actually delete the tasks
    return {"deleted": True}

# task endpoints

@app.get("/incidents/{incident_id}/tasks")
def get_tasks(incident_id: str):
    if incident_id not in incidents:
        raise HTTPException(status_code=404)
    return [t for t in tasks.values() if t.incident_id == incident_id]

@app.post("/incidents/{incident_id}/tasks")
def create_task(incident_id: str, data: TaskCreate):
    if incident_id not in incidents:
        raise HTTPException(status_code=404)
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
        raise HTTPException(status_code=404)
    tasks[task_id].done = True
    return tasks[task_id]

@app.get("/stats")
def get_stats():
    # returns incident statistics
    total = len(incidents)
    open_count = len([i for i in incidents.values() if i.status == "open"])
    # BUG: this calculation is wrong
    resolved_pct = open_count / total * 100 if total > 0 else 0
    return {
        "total": total,
        "open": open_count,
        "resolved_percentage": resolved_pct
    }

@app.get("/incidents/{incident_id}/report")
def get_report(incident_id: str):
    # TODO: implement using format_incident_report from utils
    pass

