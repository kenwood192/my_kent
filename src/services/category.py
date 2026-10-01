from sqlalchemy.orm import Session
from src.repositories.category import CategoryRepository
from src.schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema


class CategoryNotFound(Exception):
    """Category not found exception"""
    

class CategoryServices:
    def __init__(self, db: Session):
        self.db = db
        self.category_repo = CategoryRepository(db)
        
        
    def list_categories(self) -> list[CategorySchema]:
        category_orm = self.category_repo.get_all()
        return [CategorySchema.model_validate(category) for category in category_orm]
    
    def create_category(self, category_data: CategoryCreateSchema) -> CategorySchema:
        category_orm = self.category_repo.create(name=category_data.name)
        self.db.commit()
        return CategorySchema.model_validate(category_orm)
    
    def update_category(self, category_id: str, category_data: CategoryUpdateSchema) -> CategorySchema:
        category_for_update = self.category_repo.get_by_id(category_id = category_id)
        if not category_for_update:
            raise CategoryNotFound(f"Category with id {category_id} not found")
        category_for_update = self.category_repo.get_by_id(category_id=category_id)
        if category_data.name:
            assert category_for_update is not None
            category_for_update.name = category_data.name
        self.db.commit()
        self.db.refresh(category_for_update)
        return CategorySchema.model_validate(category_for_update)
    
    def delete_category(self, category_id: str) -> None:
        category_for_delete = self.category_repo.get_by_id(category_id=category_id)
        if not category_for_delete:
            raise CategoryNotFound(f"Category with id {category_id} not found")
        self.category_repo.delete(category_for_delete)
        self.db.commit()

