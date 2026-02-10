from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from mysite.db.models import Category
from mysite.db.schema import CategoryShema
from mysite.db.database import SessionLocal

category_router = APIRouter(prefix='/category', tags=['category'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@category_router.post('/create')
def category_create(category_data: CategoryShema, db: Session = Depends(get_db)):
    new_category = Category(category_name=category_data.category_name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@category_router.get('/get')
def get_category(db: Session = Depends(get_db)):
    category_db = db.query(Category).all()
    return category_db


@category_router.get('/get/{category_id}')
def category_get_detail(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Category jok")
    return category_db


@category_router.put('/update/{category_id}')
def category_update(category_id: int, category_data: CategoryShema, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Category jok")

    category_db.category_name = category_data.category_name
    db.commit()
    db.refresh(category_db)
    return category_db


@category_router.delete('/delete/{category_id}')
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Category jok")

    db.delete(category_db)
    db.commit()
    return {"message": "200 success delete"}