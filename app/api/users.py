from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.repos.userrepo import UserRepository
from app.schemas.user import UserRead
from app.auth.helpers import require_role, get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/", response_model=List[UserRead], dependencies=[Depends(require_role("admin"))])
def list_users(db: Session = Depends(get_db)):
    users = UserRepository().list_all(db)
    return users

@router.get("/me", response_model=UserRead)
def me(user = Depends(get_current_user)):
    return user
