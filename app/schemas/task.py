from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Status(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[Priority] = Priority.medium
    due_date: Optional[datetime] = None
    assignees: Optional[List[int]] = []

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[Status]
    priority: Optional[Priority]
    due_date: Optional[datetime]
    assignees: Optional[List[int]]

class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: Status
    priority: Priority
    due_date: Optional[datetime]
    created_by_id: int

    class Config:
        orm_mode = True

class BulkUpdateRequest(BaseModel):
    task_ids: list[int]
    set: dict
