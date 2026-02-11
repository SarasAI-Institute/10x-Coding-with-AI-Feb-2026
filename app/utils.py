import uuid
from datetime import datetime
from typing import List, Dict, Optional


def gen_id():
    return str(uuid.uuid4())[:8]


def get_time():
    return datetime.now()


def calculate_incident_stats(incidents_list):
    if not incidents_list:
        return {"total": 0, "by_status": {}, "by_severity": {}, "resolved_percentage": 0.0}
    
    total = len(incidents_list)
    by_status = {}
    by_severity = {}
    
    for inc in incidents_list:
        by_status[inc.status] = by_status.get(inc.status, 0) + 1
        by_severity[inc.severity] = by_severity.get(inc.severity, 0) + 1
    
    resolved = by_status.get("resolved", 0) + by_status.get("closed", 0)
    resolved_pct = (resolved / total * 100) if total > 0 else 0.0
    
    return {
        "total": total,
        "by_status": by_status,
        "by_severity": by_severity,
        "resolved_percentage": round(resolved_pct, 2)
    }


def format_incident_report(incident, tasks_list, include_tasks=True):
    severity_labels = {1: "Low", 2: "Medium-Low", 3: "Medium", 4: "High", 5: "Critical"}
    sev_label = severity_labels.get(incident.severity, "Unknown")
    
    lines = [
        "--- Incident Report ---",
        f"ID: {incident.id}",
        f"Title: {incident.title}",
        f"Severity: {incident.severity} ({sev_label})",
        f"Status: {incident.status}",
        f"Description: {incident.description}",
        f"Assigned to: {incident.assigned_to or 'Unassigned'}",
        f"Created: {incident.created_at}",
    ]
    
    if incident.tags:
        lines.append(f"Tags: {', '.join(incident.tags)}")
    
    if include_tasks:
        lines.append("")
        if tasks_list:
            lines.append("Tasks:")
            for task in sorted(tasks_list, key=lambda t: t.created_at):
                mark = "[x]" if task.done else "[ ]"
                lines.append(f"  {mark} {task.title}")
        else:
            lines.append("No tasks.")
    
    return "\n".join(lines)


def filter_incidents_by_severity(incidents_list, min_sev, max_sev):
    return [inc for inc in incidents_list if min_sev <= inc.severity <= max_sev]


def search_incidents(incidents_list, query):
    query_lower = query.lower()
    results = []
    for inc in incidents_list:
        if query_lower in inc.title.lower() or query_lower in inc.description.lower():
            results.append(inc)
        elif any(query_lower in tag.lower() for tag in inc.tags):
            results.append(inc)
    return results


def sort_incidents(incidents_list, sort_by="created_at", order="desc"):
    key_funcs = {
        "created_at": lambda x: x.created_at,
        "severity": lambda x: x.severity,
        "title": lambda x: x.title.lower(),
    }
    key_func = key_funcs.get(sort_by, key_funcs["created_at"])
    reverse = (order == "desc")
    return sorted(incidents_list, key=key_func, reverse=reverse)


def validate_severity(sev):
    return 1 <= sev <= 5


def validate_status(status):
    return status in {"open", "in_progress", "resolved", "closed"}

