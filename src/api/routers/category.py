from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_category_services
from src.schemas.category import CategoryCreateSchema, CategorySchema, CategoryUpdateSchema
from src.services.category import CategoryNotFound, CategoryServices


router = APIRouter(prefix="/categories")


@router.get("")
def read_categories(category_services: CategoryServices = Depends(get_category_services)) -> list[CategorySchema]:
    return category_services.list_categories()

@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreateSchema, category_services: CategoryServices = Depends(get_category_services)) -> CategorySchema:
    return category_services.create_category(category_data)

@router.patch("/{category_id}")
def update_category(category_id: str, category_data: CategoryUpdateSchema, category_services: CategoryServices = Depends(get_category_services)) -> CategorySchema:
    try:
        return category_services.update_category(category_id, category_data)
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, category_services: CategoryServices = Depends(get_category_services)) -> None:
    try:
        category_services.delete_category(category_id)
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))