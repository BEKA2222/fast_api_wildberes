from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Cart
from mysite.db.schema import CartShema



cart_router = APIRouter(prefix='/cart', tags=['cart'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@cart_router.post('/create')
async def create_cart(cart_data: CartShema, db: Session = Depends(get_db)):
    cart_db = Cart(**cart_data.dict())
    db.add(cart_db)
    db.commit()
    db.refresh(cart_db)
    return cart_db


@cart_router.get('/get')
async def get_carts(db: Session = Depends(get_db)):
    carts_db = db.query(Cart).all()
    return carts_db

@cart_router.get('/get/{cart_id}')
async def detail_cart(cart_id: int, db: Session = Depends(get_db)):
    cart_db = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Cart jok")
    return cart_db


@cart_router.delete('/delete/{cart_id}')
async def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart_db = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Cart jok")
    db.delete(cart_db)
    db.commit()
    return {"message": "Cart deleted successfully"}

@cart_router.put('/update/{cart_id}')
async def update_cart(cart_id: int, cart_data: CartShema, db: Session = Depends(get_db)):
    cart_db = db.query(Cart).filter(Cart.id == cart_id).first()
    if cart_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Cart jok")
    cart_db.quantity = cart_data.quantity
    db.commit()
    return cart_db