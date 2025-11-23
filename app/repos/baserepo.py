from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int):
        return db.get(self.model, id)

    def add(self, db: Session, obj):
        db.add(obj)
        db.flush()
        return obj

    def delete(self, db: Session, obj):
        db.delete(obj)
