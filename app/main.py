from fastapi import FastAPI
from app.db.session import engine, Base
from app.api import auth as auth_router, users as users_router, tasks as tasks_router
import app.models.user
import app.models.task
import app.models.task_assignment

def create_app():
    app = FastAPI(title="Task manager with FastAPI")
    app.include_router(auth_router.router)
    app.include_router(users_router.router)
    app.include_router(tasks_router.router)
    return app

app = create_app()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
