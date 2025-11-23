from app.db.session import get_db
from app.models.task import Task, StatusEnum
from app.models.assignment import task_assignments
from app.models.user import User
from app.auth.deps import require_role
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import datetime

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/overdue", dependencies=[Depends(require_role("admin", "manager"))])
def overdue_report(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    sql_query = select(User.id, User.email, func.count(Task.id).label("overdue_count")).join(task_assignments, task_assignments.c.user_id == User.id).join(Task, Task.id == task_assignments.c.task_id).where(Task.due_date < now, Task.status != StatusEnum.done).group_by(User.id, User.email)
    rows = db.execute(sql_query).all()
    return [{"user_id": r[0], "email": r[1], "overdue_count": r[2]} for r in rows]

@router.get("/distribution", dependencies=[Depends(require_role("admin", "manager"))])
def distribution(db: Session = Depends(get_db)):
    sql_query = select(User.id, User.email, Task.status, func.count(Task.id)).join(task_assignments, task_assignments.c.user_id == User.id).join(Task, Task.id == task_assignments.c.task_id).group_by(User.id, User.email, Task.status)
    rows = db.execute(sql_query).all()
    result = {}
    for user_id, email, status, cnt in rows:
        result.setdefault(user_id, {"user_id": user_id, "email": email, "counts": {}})
        result[user_id]["counts"][status.value] = cnt
    return list(result.values())
