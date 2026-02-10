from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Product
from mysite.db.schema import ProductShema


product_router = APIRouter(prefix='/product', tags=['product'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@product_router.post('/create')
async def create_product(product_data: ProductShema, db: Session = Depends(get_db)):
    product_db = Product(**product_data.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.get('/get')
async def get_products(db: Session = Depends(get_db)):
    products_db = db.query(Product).all()
    return products_db

@product_router.get('/get/{product_id}')
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if product_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Product jok")
    return product_db


@product_router.delete('/delete/{product_id}')
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if product_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Product jok")
    db.delete(product_db)
    db.commit()
    return {"message": "Product deleted successfully"}


@product_router.put('/update/{product_id}')
async def update_product(product_id: int, product_data: ProductShema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id == product_id).first()
    if product_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Product jok")
    product_db.product_name = product_data.product_name
    product_db.price = product_data.price
    product_db.category_id = product_data.category_id
    db.commit()
    db.refresh(product_db)
    return product_db
