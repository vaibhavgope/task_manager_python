# app/api/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate, BulkUpdateRequest
from app.services.task_service import TaskService
from app.repos.taskrepo import TaskRepository
from app.auth.helpers import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

task_service = TaskService(TaskRepository())

@router.post("/", response_model=TaskRead)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    t = task_service.create_task(db, user, payload)
    return t

@router.get("/", response_model=List[TaskRead])
def list_tasks(status: str | None = Query(None), priority: str | None = Query(None),
               assignee: int | None = Query(None), due_before: str | None = None,
               due_after: str | None = None, offset: int = 0, limit: int = 50,
               db: Session = Depends(get_db)):
    q = {"status": status, "priority": priority, "assignee": str(assignee) if assignee else None,
         "due_before": due_before, "due_after": due_after}
    tasks = task_service.list_tasks(db, q, offset=offset, limit=limit)
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    t = task_service.get_task(db, task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    return t

@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # permission: owner or manager/admin
    if task.created_by_id != user.id and user.role not in ("admin", "manager"):
        raise HTTPException(status_code=403, detail="Not allowed")
    updates = payload.dict(exclude_unset=True)
    # handle assignees separately if included
    assignees = updates.pop("assignees", None)
    updated_task = task_service.update_task(db, task, updates)
    if assignees is not None:
        task_service.assign_users(db, task_id, assignees)
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.created_by_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")
    from app.repos.taskrepo import TaskRepository
    repo = TaskRepository()
    repo.delete(db, task)
    db.commit()
    return None

@router.patch("/bulk_update")
def bulk_update(payload: BulkUpdateRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.role not in ("admin", "manager"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    res = task_service.bulk_update(db, payload.task_ids, payload.set)
    return res
