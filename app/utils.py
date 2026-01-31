import uuid
from datetime import datetime

def gen_id():
    return str(uuid.uuid4())[:8]

def get_time():
    return datetime.now()

# this function calculates statistics for incidents
# TODO: needs to be finished - john said he would do it but left the company
def calculate_incident_stats(incidents_list):
    return None

# formats incident for display
def format_incident_report(incident, tasks_list, include_metadata=True, format_type="text", verbose=False, include_timestamps=True, max_description_length=500, include_task_details=True, sort_tasks_by="created", include_severity_label=True, custom_header=None, custom_footer=None, indent_level=0):
    result = ""
    if custom_header is not None:
        result = result + custom_header + "\n"
    if include_metadata == True:
        if verbose == True:
            result = result + "=" * 50 + "\n"
            result = result + "INCIDENT REPORT\n"
            result = result + "=" * 50 + "\n"
        else:
            result = result + "--- Incident Report ---\n"
    if indent_level > 0:
        indent = " " * indent_level
    else:
        indent = ""
    result = result + indent + "ID: " + str(incident.id) + "\n"
    result = result + indent + "Title: " + str(incident.title) + "\n"
    if include_severity_label == True:
        if incident.severity == 1:
            sev_label = "Low"
        elif incident.severity == 2:
            sev_label = "Medium-Low"
        elif incident.severity == 3:
            sev_label = "Medium"
        elif incident.severity == 4:
            sev_label = "High"
        elif incident.severity == 5:
            sev_label = "Critical"
        else:
            sev_label = "Unknown"
        result = result + indent + "Severity: " + str(incident.severity) + " (" + sev_label + ")\n"
    else:
        result = result + indent + "Severity: " + str(incident.severity) + "\n"
    result = result + indent + "Status: " + str(incident.status) + "\n"
    desc = incident.description
    if len(desc) > max_description_length:
        desc = desc[:max_description_length] + "..."
    result = result + indent + "Description: " + desc + "\n"
    if incident.assigned_to is not None:
        result = result + indent + "Assigned to: " + str(incident.assigned_to) + "\n"
    else:
        result = result + indent + "Assigned to: Unassigned\n"
    if include_timestamps == True:
        result = result + indent + "Created: " + str(incident.created_at) + "\n"
    if len(incident.tags) > 0:
        result = result + indent + "Tags: " + ", ".join(incident.tags) + "\n"
    if include_task_details == True:
        if len(tasks_list) > 0:
            result = result + indent + "\nTasks:\n"
            if sort_tasks_by == "created":
                sorted_tasks = sorted(tasks_list, key=lambda x: x.created_at)
            elif sort_tasks_by == "title":
                sorted_tasks = sorted(tasks_list, key=lambda x: x.title)
            elif sort_tasks_by == "done":
                sorted_tasks = sorted(tasks_list, key=lambda x: x.done)
            else:
                sorted_tasks = tasks_list
            for t in sorted_tasks:
                if t.done == True:
                    status_mark = "[x]"
                else:
                    status_mark = "[ ]"
                result = result + indent + "  " + status_mark + " " + t.title
                if include_timestamps == True:
                    result = result + " (created: " + str(t.created_at) + ")"
                result = result + "\n"
        else:
            result = result + indent + "\nNo tasks.\n"
    if custom_footer is not None:
        result = result + custom_footer + "\n"
    if format_type == "text":
        return result
    elif format_type == "html":
        # convert to html - not implemented yet
        return "<pre>" + result + "</pre>"
    elif format_type == "markdown":
        # TODO: implement markdown formatting
        return result
    else:
        return result


def filter_incidents_by_severity(incidents_list, min_sev, max_sev):
    # BUG: comparison is wrong somewhere here
    result = []
    for inc in incidents_list:
        if inc.severity >= min_sev and inc.severity < max_sev:
            result.append(inc)
    return result


def search_incidents(incidents_list, query):
    # needs to be implemented
    raise NotImplementedError("search not implemented")


def get_overdue_tasks(tasks_list, incidents_dict):
    # TODO: implement this - should return tasks for incidents that are still open after 7 days
    pass


def sort_incidents(incidents_list, sort_by="created_at", order="desc"):
    if sort_by == "created_at":
        s = sorted(incidents_list, key=lambda x: x.created_at)
    elif sort_by == "severity":
        s = sorted(incidents_list, key=lambda x: x.severity)
    elif sort_by == "title":
        s = sorted(incidents_list, key=lambda x: x.title)
    else:
        s = incidents_list
    # BUG: order parameter is ignored, always returns ascending
    return s


def validate_severity(sev):
    if sev < 1:
        return False
    if sev > 5:
        return False
    return True

