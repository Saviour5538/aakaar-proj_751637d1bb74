from typing import Type, TypeVar, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

T = TypeVar("T")

class CRUDService:
    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, db: Session, obj_data: dict) -> T:
        try:
            obj = self.model(**obj_data)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Error creating {self.model.__name__}: {str(e)}")

    def read(self, db: Session, obj_id: str) -> Optional[T]:
        try:
            return db.query(self.model).filter(self.model.id == obj_id).first()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error reading {self.model.__name__}: {str(e)}")

    def update(self, db: Session, obj_id: str, obj_data: dict) -> Optional[T]:
        try:
            obj = db.query(self.model).filter(self.model.id == obj_id).first()
            if not obj:
                return None
            for key, value in obj_data.items():
                setattr(obj, key, value)
            db.commit()
            db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Error updating {self.model.__name__}: {str(e)}")

    def delete(self, db: Session, obj_id: str) -> bool:
        try:
            obj = db.query(self.model).filter(self.model.id == obj_id).first()
            if not obj:
                return False
            db.delete(obj)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Error deleting {self.model.__name__}: {str(e)}")

    def list(self, db: Session) -> List[T]:
        try:
            return db.execute(select(self.model)).scalars().all()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Error listing {self.model.__name__}: {str(e)}")