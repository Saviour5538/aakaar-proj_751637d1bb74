from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from database.models import Todo
from database.config import get_db
from backend.services.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/todos")

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    completed: Optional[bool] = None

class TodoResponse(TodoBase):
    id: UUID
    user_id: UUID
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

@router.get("/", response_model=List[TodoResponse], operation_id="listTodos")
async def list_todos(db: Session = Depends(get_db), current_user: UUID = Depends(get_current_user)):
    todos = db.query(Todo).filter(Todo.user_id == current_user).all()
    return todos

@router.post("/", response_model=TodoResponse, operation_id="createTodo")
async def create_todo(todo_data: TodoCreate, db: Session = Depends(get_db), current_user: UUID = Depends(get_current_user)):
    new_todo = Todo(
        user_id=current_user,
        title=todo_data.title,
        description=todo_data.description,
        due_date=todo_data.due_date,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/{id}", response_model=TodoResponse, operation_id="getTodo")
async def get_todo(id: UUID, db: Session = Depends(get_db), current_user: UUID = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == current_user).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo

@router.put("/{id}", response_model=TodoResponse, operation_id="updateTodo")
async def update_todo(id: UUID, todo_data: TodoUpdate, db: Session = Depends(get_db), current_user: UUID = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == current_user).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.due_date = todo_data.due_date
    todo.completed = todo_data.completed if todo_data.completed is not None else todo.completed
    todo.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(todo)
    return todo

@router.patch("/{id}", response_model=TodoResponse, operation_id="toggleTodo")
async def toggle_todo(id: UUID, db: Session = Depends(get_db), current_user: UUID = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == current_user).with_for_update().first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    todo.completed = not todo.completed
    todo.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, operation_id="deleteTodo")
async def delete_todo(id: UUID, db: Session = Depends(get_db), current_user: UUID = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == current_user).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return None