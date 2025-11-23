from passlib.context import CryptContext
from app.repos.userrepo import UserRepository
from sqlalchemy.orm import Session
from app.models.user import User

pwd_ctx = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, db: Session, email: str, password: str, full_name: str | None = None, role: str = "member"):
        existing_user = self.repo.get_by_email(db, email)
        if existing_user:
            raise ValueError("User already exists")
        user = User(email=email, full_name=full_name, hashed_password=pwd_ctx.hash(password), role=role)
        self.repo.add(db, user)
        db.commit()
        db.refresh(user)
        return user

    def authenticate(self, db: Session, email: str, password: str):
        user = self.repo.get_by_email(db, email)
        if not user or not pwd_ctx.verify(password, user.hashed_password):
            return None
        return user
