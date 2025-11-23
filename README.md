# Task Manager API

Task manager API build with FastAPI + Python + SQLite

## Functionality supported

- User signup + login (JWT)
- Task CRUD
- Bulk update on tasks
- Filtering tasks by:
  - status (supports CSV OR)
  - priority (CSV OR)
  - assignee
  - due_before / due_after dates  
- Reports (overdue + distribution)

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Running the server:
```bash
uvicorn app.main:app --reload
```

Swagger UI:
```http://127.0.0.1:8000/docs```

### Main routes and usage:

```
POST /api/auth/signup
{
  "email": "test@example.com",
  "full_name": "Test",
  "password": "pass"
}
```

```
POST /api/auth/login
username=test@example.com&password=pass
```

```
POST /api/tasks
Authorization: Bearer <token>
{
  "title": "some task",
  "priority": "high"
}
```
Basic Filtering:
```
/api/tasks?status=todo,in_progress&priority=high&assignee=1&due_before=2025-01-01
```

Bulk update tasks:
```
PATCH /api/tasks/bulk_update
{
  "task_ids": [1, 2],
  "set": { "status": "in_progress" }
}
```

Reports

```
GET /api/reports/overdue
GET /api/reports/distribution
```



### Design considerations and limitations:

- Filtering logic is very basic currently and needs refinement and additional routes to accept nested filters in body.
- Chosen optional features are listed below. The reason is relative importance of these features compared to other options. Making tasks dependent on each other could be implemented next but would require some more design considerations and tables.
    - Filtering
    - API showing task distribution and overdue tasks
- SQLite is chosen as DB for simplicity and ease of use. Adding support for containerization would allow us to use other DBs like Postgres or MySQL.
- JWT is used for authentication due to minimal setup and simplicity.
- Most of the design/modules are chosen not necessarily for production readyness but simplicity due to time constraints.
