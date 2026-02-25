# Task Board - API Specification

## Base URL
```
http://localhost:8000
```

## Endpoints

### GET /tasks
List all tasks.

**Response:** `200 OK`
```json
{
  "tasks": [
    {
      "id": "abc123",
      "title": "Task title",
      "description": "Optional description",
      "column": "todo",
      "created_at": "2025-01-09T10:00:00",
      "updated_at": "2025-01-09T10:00:00"
    }
  ],
  "total": 1
}
```

---

### GET /tasks/{task_id}
Get a single task by ID.

**Response:** `200 OK`
```json
{
  "id": "abc123",
  "title": "Task title",
  "description": "Optional description",
  "column": "todo",
  "created_at": "2025-01-09T10:00:00",
  "updated_at": "2025-01-09T10:00:00"
}
```

**Error:** `404 Not Found`
```json
{
  "detail": "Task not found"
}
```

---

### POST /tasks
Create a new task.

**Request:**
```json
{
  "title": "Task title",
  "description": "Optional description"
}
```

**Response:** `201 Created`
```json
{
  "id": "abc123",
  "title": "Task title",
  "description": "Optional description",
  "column": "todo",
  "created_at": "2025-01-09T10:00:00",
  "updated_at": "2025-01-09T10:00:00"
}
```

**Error:** `400 Bad Request`
```json
{
  "detail": "Title is required"
}
```

---

### PATCH /tasks/{task_id}
Update a task.

**Request:**
```json
{
  "title": "Updated title",
  "description": "Updated description"
}
```

**Response:** `200 OK`
```json
{
  "id": "abc123",
  "title": "Updated title",
  "description": "Updated description",
  "column": "todo",
  "created_at": "2025-01-09T10:00:00",
  "updated_at": "2025-01-09T11:00:00"
}
```

---

### PATCH /tasks/{task_id}/move
Move a task to a different column.

**Request:**
```json
{
  "column": "in_progress"
}
```

**Response:** `200 OK`
```json
{
  "id": "abc123",
  "title": "Task title",
  "description": "Description",
  "column": "in_progress",
  "created_at": "2025-01-09T10:00:00",
  "updated_at": "2025-01-09T11:00:00"
}
```

**Error:** `400 Bad Request`
```json
{
  "detail": "Invalid column. Must be one of: todo, in_progress, done"
}
```

---

### DELETE /tasks/{task_id}
Delete a task.

**Response:** `200 OK`
```json
{
  "deleted": true
}
```

---

### GET /board
Get board view with tasks grouped by column.

**Response:** `200 OK`
```json
{
  "columns": {
    "todo": [
      {"id": "abc123", "title": "Task 1", ...}
    ],
    "in_progress": [
      {"id": "def456", "title": "Task 2", ...}
    ],
    "done": []
  },
  "stats": {
    "total": 2,
    "todo": 1,
    "in_progress": 1,
    "done": 0
  }
}
```

---

## Column Values

Valid column values:
- `todo` - To Do
- `in_progress` - In Progress
- `done` - Done

---

## Error Responses

All errors return JSON with a `detail` field:

```json
{
  "detail": "Error message here"
}
```

| Status Code | Meaning |
|-------------|---------|
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource doesn't exist |
| 422 | Validation Error - Invalid data format |

