from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import SubCategory
from mysite.db.schema import SubCategoryShema



subcategory_router = APIRouter(prefix='/subcategory', tags=['subcategory'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@subcategory_router.post('/create')
async def create_sub_category(sub_data: SubCategoryShema, db: Session = Depends(get_db)):
    sub_db = SubCategory(**sub_data.dict())
    db.add(sub_db)
    db.commit()
    db.refresh(sub_db)
    return sub_db


@subcategory_router.get('/get')
async def get_sub(db: Session = Depends(get_db)):
    sub_db = db.query(SubCategory).all()
    return sub_db


@subcategory_router.get('/get/{sub_id}')
async def get_sub_by_id(sub_id: int, db: Session = Depends(get_db)):
    sub_db = db.query(SubCategory).filter(SubCategory.id == sub_id).first()
    if not sub_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subcategory not found")
    return sub_db


@subcategory_router.delete('/delete/{sub_id}')
async def delete_sub_category(sub_id: int, db: Session = Depends(get_db)):
    sub_db = db.query(SubCategory).filter(SubCategory.id == sub_id).first()
    if not sub_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subcategory not found")
    db.delete(sub_db)
    db.commit()
    return {"message": "Subcategory deleted successfully"}


@subcategory_router.put('/update/{sub_id}')
async def update_sub_category(sub_id: int, sub_data: SubCategoryShema, db: Session = Depends(get_db)):
    sub_db = db.query(SubCategory).filter(SubCategory.id == sub_id).first()
    if not sub_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subcategory not found")
    sub_db.subcategory_name = sub_data.subcategory_name
    db.commit()
    db.refresh(sub_db)
    return sub_db