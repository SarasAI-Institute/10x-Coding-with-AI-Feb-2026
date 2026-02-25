# Task Board - Frontend Specification

## Technology Stack
- React 18+
- Vite (build tool)
- Vanilla CSS or Tailwind CSS
- Fetch API for HTTP requests

## Layout

### Overall Structure
```
┌─────────────────────────────────────────────────────────────┐
│  Header: "Task Board"                           [Stats]     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   To Do     │  │ In Progress │  │    Done     │         │
│  │             │  │             │  │             │         │
│  │  [+ Add]    │  │             │  │             │         │
│  │             │  │             │  │             │         │
│  │  ┌───────┐  │  │  ┌───────┐  │  │  ┌───────┐  │         │
│  │  │ Task  │  │  │  │ Task  │  │  │  │ Task  │  │         │
│  │  │ Card  │  │  │  │ Card  │  │  │  │ Card  │  │         │
│  │  └───────┘  │  │  └───────┘  │  │  └───────┘  │         │
│  │             │  │             │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. App (Root)
- Fetches tasks on mount
- Manages global state
- Renders Header and Board

### 2. Header
- Displays "Task Board" title
- Shows statistics (total tasks, per column)

### 3. Board
- Container for all three columns
- Flexbox layout, horizontal arrangement

### 4. Column
Props: `title`, `columnId`, `tasks`, `onAddTask`, `onMoveTask`
- Displays column header
- "Add Task" button (only for To Do column)
- Renders list of TaskCards

### 5. TaskCard
Props: `task`, `onEdit`, `onMove`, `onDelete`
- Displays task title
- Truncated description (max 50 chars)
- Move buttons (← →) or dropdown
- Edit and Delete buttons

### 6. TaskForm (Modal)
Props: `task` (optional), `onSave`, `onCancel`
- Title input (required)
- Description textarea
- Save and Cancel buttons
- Used for both create and edit

## Styling Guidelines

### Colors
- Background: `#f5f5f5` (light gray)
- Columns: `#ffffff` (white)
- To Do: `#e3f2fd` (light blue header)
- In Progress: `#fff3e0` (light orange header)
- Done: `#e8f5e9` (light green header)
- Cards: `#ffffff` with subtle shadow

### Typography
- Font: System fonts (sans-serif)
- Title: 24px bold
- Column headers: 16px semibold
- Card title: 14px medium
- Card description: 12px regular, gray

### Spacing
- Column gap: 16px
- Card gap: 8px
- Card padding: 12px
- Border radius: 8px

## Interactions

### Add Task
1. Click "Add Task" button
2. Modal appears with form
3. Fill title (required) and description
4. Click Save → Task appears in To Do
5. Click Cancel → Modal closes

### Move Task
1. Click move button (→) on task
2. Task moves to next column
3. Or use dropdown to select column

### Edit Task
1. Click task card
2. Modal appears with current values
3. Modify fields
4. Save updates task

### Delete Task
1. Click delete button on task
2. Confirmation dialog appears
3. Confirm → Task is removed

## API Integration

Base URL: `http://localhost:8000`

```javascript
// Fetch all tasks
const response = await fetch('/board');
const data = await response.json();

// Create task
await fetch('/tasks', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ title, description })
});

// Move task
await fetch(`/tasks/${taskId}/move`, {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ column: newColumn })
});

// Delete task
await fetch(`/tasks/${taskId}`, { method: 'DELETE' });
```

## State Management

Simple React state with `useState`:
```javascript
const [tasks, setTasks] = useState({ todo: [], in_progress: [], done: [] });
const [stats, setStats] = useState({ total: 0, todo: 0, in_progress: 0, done: 0 });
const [isModalOpen, setIsModalOpen] = useState(false);
const [editingTask, setEditingTask] = useState(null);
```

## Responsive Design

- Desktop: Three columns side by side
- Tablet: Three columns, narrower
- Mobile: Stack columns vertically (nice to have)

