from fastapi import Depends
from sqlalchemy.orm import Session
from src.services.task import TaskServices
from src.services.category import CategoryServices
from src.db.session import get_db


def get_task_services(db: Session = Depends(get_db)) -> TaskServices:
    return TaskServices(db)


def get_category_services(db: Session = Depends(get_db)) -> CategoryServices:
    return CategoryServices(db)