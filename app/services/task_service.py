# app/services/task_service.py
from app.repos.taskrepo import TaskRepository
from sqlalchemy.orm import Session
from app.models.task import Task, StatusEnum, PriorityEnum
from app.models.task_assignment import task_assignments
from app.models.user import User
from typing import List
from datetime import datetime
from sqlalchemy import select

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create_task(self, db: Session, creator: User, payload):
        t = Task(
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            due_date=payload.due_date,
            created_by_id=creator.id
        )
        self.repo.create(db, t)
        if payload.assignees:
            self.repo.assign_users(db, t.id, payload.assignees)
        db.commit()
        db.refresh(t)
        return t

    def get_task(self, db: Session, task_id: int):
        return self.repo.get(db, task_id)

    def list_tasks(self, db: Session, query_params: dict, offset=0, limit=50):
        filters = []

        if status := query_params.get("status"):
            vals = [s.strip() for s in status.split(",")]
            filters.append(Task.status.in_(vals))

        if priority := query_params.get("priority"):
            vals = [s.strip() for s in priority.split(",")]
            filters.append(Task.priority.in_(vals))

        if created_by := query_params.get("created_by"):
            filters.append(Task.created_by_id == int(created_by))

        if due_before := query_params.get("due_before"):
            filters.append(Task.due_date <= datetime.fromisoformat(due_before))
        if due_after := query_params.get("due_after"):
            filters.append(Task.due_date >= datetime.fromisoformat(due_after))

        if assignee := query_params.get("assignee"):
            sql_result = select(Task).join(task_assignments).where(task_assignments.c.user_id == int(assignee))
            return db.execute(sql_result.offset(offset).limit(limit)).scalars().all()

        return self.repo.list(db, filters, offset=offset, limit=limit)

    def update_task(self, db: Session, task: Task, updates: dict):
        allowed = {"title", "description", "status", "priority", "due_date"}
        for k, v in updates.items():
            if k not in allowed:
                continue
            if k == "status":
                task.status = StatusEnum(v)
            elif k == "priority":
                task.priority = PriorityEnum(v)
            else:
                setattr(task, k, v)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def bulk_update(self, db: Session, task_ids: List[int], values: dict):
        allowed = {"status", "priority", "due_date", "title", "description"}
        to_set = {}
        for k, v in values.items():
            if k not in allowed:
                continue
            if k == "status":
                to_set["status"] = StatusEnum(v)
            elif k == "priority":
                to_set["priority"] = PriorityEnum(v)
            else:
                to_set[k] = v
        if not to_set:
            return {"updated": 0}
        count = self.repo.bulk_update(db, task_ids, to_set)
        db.commit()
        return {"updated": count}

    def assign_users(self, db: Session, task_id: int, user_ids: List[int]):
        self.repo.assign_users(db, task_id, user_ids)
        db.commit()
