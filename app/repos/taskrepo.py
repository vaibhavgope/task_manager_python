from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, update
from app.models.task import Task
from app.models.task_assignment import task_assignments
from typing import List

class TaskRepository:
    def get(self, db: Session, id: int):
        return db.get(Task, id)

    def create(self, db: Session, task: Task):
        db.add(task)
        db.flush()
        return task

    def list(self, db: Session, filters=None, offset=0, limit=50):
        sql_result = select(Task)
        if filters:
            sql_result = sql_result.where(*filters)
        sql_result = sql_result.offset(offset).limit(limit)
        return db.execute(sql_result.options(selectinload(Task.created_by))).scalars().all()

    def bulk_update(self, db: Session, task_ids: List[int], values: dict):
        sql_result = update(Task).where(Task.id.in_(task_ids)).values(**values)
        result = db.execute(sql_result)
        return result.rowcount

    def assign_users(self, db: Session, task_id: int, user_ids: List[int]):
        db.execute(task_assignments.delete().where(task_assignments.c.task_id == task_id))
        values = [{"task_id": task_id, "user_id": uid} for uid in user_ids]
        if values:
            db.execute(task_assignments.insert(), values)
