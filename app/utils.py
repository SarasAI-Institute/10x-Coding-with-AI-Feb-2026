"""Utility functions for the Incident Management API."""
import uuid
from datetime import datetime
from typing import List, Dict
from app.models import Incident, Task


def gen_id() -> str:
    """Generate a short unique identifier."""
    return str(uuid.uuid4())[:8]


def get_time() -> datetime:
    """Get the current timestamp."""
    return datetime.now()


def validate_severity(severity: int) -> bool:
    """Validate severity is between 1 and 5."""
    return 1 <= severity <= 5


def validate_status(status: str) -> bool:
    """Validate status is a valid value."""
    return status in {"open", "in_progress", "resolved", "closed"}


def sort_incidents(incidents_list: List[Incident], sort_by: str = "created_at", order: str = "desc") -> List[Incident]:
    """Sort incidents by specified field."""
    key_funcs = {
        "created_at": lambda x: x.created_at,
        "severity": lambda x: x.severity,
        "title": lambda x: x.title.lower(),
    }
    key_func = key_funcs.get(sort_by, key_funcs["created_at"])
    reverse = (order == "desc")
    return sorted(incidents_list, key=key_func, reverse=reverse)


def calculate_incident_stats(incidents_list: List[Incident]) -> Dict:
    """Calculate statistics for incidents."""
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


def format_incident_report(incident: Incident, tasks_list: List[Task]) -> str:
    """Format incident as a text report."""
    severity_labels = {1: "Low", 2: "Medium-Low", 3: "Medium", 4: "High", 5: "Critical"}
    sev_label = severity_labels.get(incident.severity, "Unknown")
    
    lines = [
        "--- Incident Report ---",
        f"ID: {incident.id}",
        f"Title: {incident.title}",
        f"Severity: {incident.severity} ({sev_label})",
        f"Status: {incident.status}",
    ]
    
    if tasks_list:
        lines.append("\nTasks:")
        for task in tasks_list:
            mark = "[x]" if task.done else "[ ]"
            lines.append(f"  {mark} {task.title}")
    
    return "\n".join(lines)


# =============================================================================
# NEW CODE ADDED BY TEAMMATE - needs refactoring
# =============================================================================

def export_incidents_to_csv(incidents_list, include_tasks=True, tasks_dict=None, delimiter=",", include_header=True, date_format="%Y-%m-%d %H:%M", include_id=True, include_description=True, max_description_length=100, include_tags=True, include_assigned=True, include_escalation=True):
    """Export incidents to CSV format - added quickly, needs cleanup."""
    result = ""
    if include_header:
        header_parts = []
        if include_id:
            header_parts.append("id")
        header_parts.append("title")
        if include_description:
            header_parts.append("description")
        header_parts.append("severity")
        header_parts.append("status")
        header_parts.append("created_at")
        if include_assigned:
            header_parts.append("assigned_to")
        if include_tags:
            header_parts.append("tags")
        if include_escalation:
            header_parts.append("escalation_level")
        if include_tasks:
            header_parts.append("task_count")
            header_parts.append("tasks_done")
        result = delimiter.join(header_parts) + "\n"
    for inc in incidents_list:
        row_parts = []
        if include_id:
            row_parts.append(inc.id)
        row_parts.append('"' + inc.title.replace('"', '""') + '"')
        if include_description:
            desc = inc.description
            if len(desc) > max_description_length:
                desc = desc[:max_description_length] + "..."
            row_parts.append('"' + desc.replace('"', '""') + '"')
        row_parts.append(str(inc.severity))
        row_parts.append(inc.status)
        row_parts.append(inc.created_at.strftime(date_format))
        if include_assigned:
            row_parts.append(inc.assigned_to or "")
        if include_tags:
            row_parts.append('"' + ";".join(inc.tags) + '"')
        if include_escalation:
            row_parts.append(str(inc.escalation_level))
        if include_tasks and tasks_dict:
            inc_tasks = [t for t in tasks_dict.values() if t.incident_id == inc.id]
            row_parts.append(str(len(inc_tasks)))
            row_parts.append(str(len([t for t in inc_tasks if t.done])))
        elif include_tasks:
            row_parts.append("0")
            row_parts.append("0")
        result = result + delimiter.join(row_parts) + "\n"
    return result


def process_bulk_incidents(incidents_data, storage_dict, auto_assign=False, default_assignee=None, validate_all=True, stop_on_error=False, generate_ids=True, set_status="open", notify=False, notification_list=None):
    """Process bulk incident creation - messy implementation."""
    results = []
    errors = []
    for i, data in enumerate(incidents_data):
        try:
            if validate_all:
                if not data.title or len(data.title) < 1:
                    if stop_on_error:
                        raise ValueError(f"Item {i}: Title required")
                    else:
                        errors.append({"index": i, "error": "Title required"})
                        continue
                if not validate_severity(data.severity):
                    if stop_on_error:
                        raise ValueError(f"Item {i}: Invalid severity")
                    else:
                        errors.append({"index": i, "error": "Invalid severity"})
                        continue
            if generate_ids:
                inc_id = gen_id()
            else:
                inc_id = str(i)
            assignee = data.assigned_to
            if auto_assign and not assignee:
                assignee = default_assignee
            from app.models import Incident
            inc = Incident(
                id=inc_id,
                title=data.title,
                description=data.description,
                severity=data.severity,
                status=set_status,
                created_at=get_time(),
                assigned_to=assignee,
                tags=data.tags,
                escalation_level=0
            )
            storage_dict[inc.id] = inc
            results.append(inc)
            if notify and notification_list is not None:
                notification_list.append({"type": "created", "incident_id": inc.id})
        except Exception as e:
            if stop_on_error:
                raise
            errors.append({"index": i, "error": str(e)})
    return {"created": results, "errors": errors, "total": len(incidents_data), "success_count": len(results), "error_count": len(errors)}


def handle_escalation(incident, escalation_request, escalation_history_dict, notification_log_list, max_level=3, auto_reassign=False, reassign_to=None, update_severity=True, severity_increment=1, notify_on_escalation=True):
    """Handle incident escalation - complex and needs simplification."""
    current_level = incident.escalation_level
    if current_level >= max_level:
        return {"success": False, "error": "Maximum escalation level reached", "current_level": current_level}
    new_level = current_level + 1
    incident.escalation_level = new_level
    if update_severity and incident.severity < 5:
        new_severity = min(5, incident.severity + severity_increment)
        incident.severity = new_severity
    if auto_reassign and reassign_to:
        incident.assigned_to = reassign_to
    if incident.id not in escalation_history_dict:
        escalation_history_dict[incident.id] = []
    escalation_record = {
        "timestamp": get_time().isoformat(),
        "from_level": current_level,
        "to_level": new_level,
        "reason": escalation_request.reason,
        "severity_updated": update_severity
    }
    escalation_history_dict[incident.id].append(escalation_record)
    if notify_on_escalation:
        for email in escalation_request.notify_emails:
            notification_log_list.append({
                "type": "escalation",
                "incident_id": incident.id,
                "email": email,
                "level": new_level,
                "timestamp": get_time().isoformat()
            })
    return {"success": True, "new_level": new_level, "incident": incident}


def send_notification(notification_type, incident_id, recipients, message=None, priority="normal", log_list=None, include_timestamp=True, include_incident_details=False, incident_dict=None):
    """Send notification - stub implementation, very messy."""
    notifications_sent = []
    for r in recipients:
        notif = {"type": notification_type, "incident_id": incident_id, "recipient": r, "priority": priority}
        if message:
            notif["message"] = message
        if include_timestamp:
            notif["timestamp"] = get_time().isoformat()
        if include_incident_details and incident_dict and incident_id in incident_dict:
            inc = incident_dict[incident_id]
            notif["incident_title"] = inc.title
            notif["incident_severity"] = inc.severity
            notif["incident_status"] = inc.status
        notifications_sent.append(notif)
        if log_list is not None:
            log_list.append(notif)
    return {"sent": len(notifications_sent), "notifications": notifications_sent}

