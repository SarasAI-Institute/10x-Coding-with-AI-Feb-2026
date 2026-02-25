# Task Board - User Stories

## Epic: Task Management

### US-1: View Board
**As a** user  
**I want to** see all tasks organized by column  
**So that** I can understand the status of my work  

**Acceptance Criteria:**
- [ ] Board displays three columns: To Do, In Progress, Done
- [ ] Each column shows its tasks
- [ ] Empty columns show a placeholder message
- [ ] Tasks show title and truncated description

---

### US-2: Create Task
**As a** user  
**I want to** create a new task  
**So that** I can track work I need to do  

**Acceptance Criteria:**
- [ ] "Add Task" button visible in To Do column
- [ ] Clicking opens a form with title and description fields
- [ ] Title is required, description is optional
- [ ] Submitting creates task in "To Do" column
- [ ] New task appears immediately without page refresh

---

### US-3: Move Task
**As a** user  
**I want to** move a task to a different column  
**So that** I can update its status  

**Acceptance Criteria:**
- [ ] Each task has buttons/dropdown to change column
- [ ] Moving a task updates it immediately
- [ ] Task appears in new column without refresh

---

### US-4: Edit Task
**As a** user  
**I want to** edit a task's details  
**So that** I can update information  

**Acceptance Criteria:**
- [ ] Clicking a task opens edit view
- [ ] Can modify title and description
- [ ] Save button updates the task
- [ ] Cancel button discards changes

---

### US-5: Delete Task
**As a** user  
**I want to** delete a task  
**So that** I can remove completed or irrelevant work  

**Acceptance Criteria:**
- [ ] Delete button visible on each task
- [ ] Confirmation before deleting
- [ ] Task removed immediately after confirmation

---

## Epic: Board Statistics

### US-6: View Statistics
**As a** user  
**I want to** see task statistics  
**So that** I can understand my workload  

**Acceptance Criteria:**
- [ ] Display total task count
- [ ] Display count per column
- [ ] Statistics update when tasks change

