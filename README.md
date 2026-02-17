# Incident Management API

A FastAPI application for tracking and managing operational incidents and tasks.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

API at http://localhost:8000 | Docs at http://localhost:8000/docs

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /incidents | List incidents |
| POST | /incidents | Create incident |
| GET | /incidents/{id} | Get incident |
| PATCH | /incidents/{id}/status | Update status |
| DELETE | /incidents/{id} | Delete incident |
| GET | /incidents/{id}/tasks | List tasks |
| POST | /incidents/{id}/tasks | Create task |
| GET | /stats | Get statistics |
| POST | /incidents/bulk | Bulk create (NEW) |
| GET | /incidents/export | Export to CSV (NEW) |
| POST | /incidents/{id}/escalate | Escalate incident (NEW) |

## Running Tests

```bash
pytest tests/ -v
```

## Recent Changes

A teammate added some new features while you were away:
- Bulk incident creation
- CSV export
- Incident escalation
- Notification system

These features work but could use some cleanup...

