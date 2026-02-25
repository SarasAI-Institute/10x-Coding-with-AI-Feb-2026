# Task Board - Requirements

## Overview

A simple Kanban-style task board for managing tasks across columns.

## Functional Requirements

### FR-1: Column Management
- System must support exactly 3 columns: "To Do", "In Progress", "Done"
- Columns are predefined and cannot be created/deleted by users

### FR-2: Task Management
- Users can create tasks with a title and optional description
- Users can view all tasks organized by column
- Users can move tasks between columns
- Users can edit task title and description
- Users can delete tasks
- Tasks should display creation date

### FR-3: Task Properties
- Each task must have:
  - Unique ID (auto-generated)
  - Title (required, 1-100 characters)
  - Description (optional, max 500 characters)
  - Column (one of: todo, in_progress, done)
  - Created timestamp
  - Updated timestamp

### FR-4: Board View
- Display all three columns side by side
- Show tasks within their respective columns
- Allow drag-and-drop to move tasks (nice to have)
- Click to edit task details

## Non-Functional Requirements

### NFR-1: Performance
- API responses under 100ms
- Frontend loads in under 2 seconds

### NFR-2: Technology Stack
- Backend: Python 3.11+, FastAPI
- Frontend: React 18+, Vite
- Storage: In-memory (no database)

### NFR-3: API Design
- RESTful API design
- JSON request/response format
- Proper HTTP status codes
- CORS enabled for frontend

## Out of Scope
- User authentication
- Persistent storage
- Multiple boards
- Custom columns
- Task assignments
- Due dates

