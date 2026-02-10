from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import ImageProduct
from mysite.db.schema import ImageProductShema



imageproduct_router = APIRouter(prefix='/imageproduct', tags=['imageproduct'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@imageproduct_router.post('/create')
async def create_imageproduct(imageproduct_data: ImageProductShema, db: Session = Depends(get_db)):
    imageproduct_db = ImageProduct(**imageproduct_data.dict())
    db.add(imageproduct_db)
    db.commit()
    db.refresh(imageproduct_db)
    return imageproduct_db



@imageproduct_router.get('/get')
async def get_imageproducts(db: Session = Depends(get_db)):
    imageproducts_db = db.query(ImageProduct).all()
    return imageproducts_db



@imageproduct_router.get('/get/{imageproduct_id}')
async def detail_imageproduct(imageproduct_id: int, db: Session = Depends(get_db)):
    imageproduct_db = db.query(ImageProduct).filter(ImageProduct.id == imageproduct_id).first()
    if imageproduct_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Imageproduct jok")
    return imageproduct_db



@imageproduct_router.delete('/delete/{imageproduct_id}')
async def delete_imageproduct(imageproduct_id: int, db: Session = Depends(get_db)):
    imageproduct_db = db.query(ImageProduct).filter(ImageProduct.id == imageproduct_id).first()
    if imageproduct_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Imageproduct jok")
    db.delete(imageproduct_db)
    db.commit()
    return {"message": "Imageproduct deleted successfully"}


@imageproduct_router.put('/update/{imageproduct_id}')
async def update_imageproduct(imageproduct_id: int, imageproduct_data: ImageProductShema, db: Session = Depends(get_db)):
    imageproduct_db = db.query(ImageProduct).filter(ImageProduct.id == imageproduct_id).first()
    if imageproduct_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Imageproduct jok")
    imageproduct_db.name = imageproduct_data.name
    imageproduct_db.description = imageproduct_data.description
    imageproduct_db.price = imageproduct_data.price
    imageproduct_db.image_url = imageproduct_data.image_url
    db.commit()
    return imageproduct_db

