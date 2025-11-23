from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.repos.baserepo import BaseRepository
from typing import Optional

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        sql_result = select(User).where(User.email == email)
        return db.execute(sql_result).scalars().first()

    def list_all(self, db: Session, offset: int = 0, limit: int = 100):
        sql_result = select(User).offset(offset).limit(limit)
        return db.execute(sql_result).scalars().all()
