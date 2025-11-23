from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.session import Base

task_assignments = Table(
    "task_assignments",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)
