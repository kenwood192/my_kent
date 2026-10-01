from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_task_services
from src.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from src.services.task import TaskNotFound, TaskServices

router = APIRouter(prefix="/tasks")



@router.get("")
def read_tasks(task_services: TaskServices = Depends(get_task_services)) -> list[TaskSchema]:
    return task_services.list_tasks()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, 
                task_services: TaskServices = Depends(get_task_services)
                ) -> TaskSchema:
    return task_services.create_task(task_create=payload)

@router.patch("/{task_id}")
def update_task(task_id: str, 
                payload: TaskUpdateSchema, 
                task_services: TaskServices = Depends(get_task_services)
                ) -> TaskSchema:
    try:
        return task_services.update_task(task_id=task_id, task_update=payload)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Task with id {task_id} not found")


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str,
                task_services: TaskServices = Depends(get_task_services)
                ) -> None:
    try:    
        return task_services.delete_task(task_id=task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Task with id {task_id} not found")