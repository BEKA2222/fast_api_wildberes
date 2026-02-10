from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import CartItem
from mysite.db.schema import CartItemShema



cartitem_router = APIRouter(prefix='/cartitem', tags=['cartitem'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@cartitem_router.post('/create')
async def create_cartitem(cartitem_data: CartItemShema, db: Session = Depends(get_db)):
    cartitem_db = CartItem(**cartitem_data.dict())
    db.add(cartitem_db)
    db.commit()
    db.refresh(cartitem_db)
    return cartitem_db


@cartitem_router.get('/get')
async def get_cartitems(db: Session = Depends(get_db)):
    cartitems_db = db.query(CartItem).all()
    return cartitems_db


@cartitem_router.get('/get/{cartitem_id}')
async def detail_cartitem(cartitem_id: int, db: Session = Depends(get_db)):
    cartitem_db = db.query(CartItem).filter(CartItem.id == cartitem_id).first()
    if cartitem_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai CartItem jok")
    return cartitem_db


@cartitem_router.delete('/delete/{cartitem_id}')
async def delete_cartitem(cartitem_id: int, db: Session = Depends(get_db)):
    cartitem_db = db.query(CartItem).filter(CartItem.id == cartitem_id).first()
    if cartitem_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai CartItem jok")
    db.delete(cartitem_db)
    db.commit()
    return {"message": "CartItem deleted successfully"}

@cartitem_router.put('/update/{cartitem_id}')
async def update_cartitem(cartitem_id: int, cartitem_data: CartItemShema, db: Session = Depends(get_db)):
    cartitem_db = db.query(CartItem).filter(CartItem.id == cartitem_id).first()
    if cartitem_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai CartItem jok")
    cartitem_db.product_id = cartitem_data.product_id
    cartitem_db.user_id = cartitem_data.user_id
    cartitem_db.quantity = cartitem_data.quantity
    db.commit()
    db.refresh(cartitem_db)
    return cartitem_db