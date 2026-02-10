from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import FavoriteItem
from mysite.db.schema import FavoriteItemShema



favoriteitem_router = APIRouter(prefix='/favoriteitem', tags=['favoriteitem'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@favoriteitem_router.post('/create')
async def create_favoriteitem(favoriteitem_data: FavoriteItemShema, db: Session = Depends(get_db)):
    favoriteitem_db = FavoriteItem(**favoriteitem_data.dict())
    db.add(favoriteitem_db)
    db.commit()
    db.refresh(favoriteitem_db)
    return favoriteitem_db


@favoriteitem_router.get('/get')
async def get_favoriteitems(db: Session = Depends(get_db)):
    favoriteitems_db = db.query(FavoriteItem).all()
    return favoriteitems_db

@favoriteitem_router.get('/get/{favoriteitem_id}')
async def detail_favoriteitem(favoriteitem_id: int, db: Session = Depends(get_db)):
    favoriteitem_db = db.query(FavoriteItem).filter(FavoriteItem.id == favoriteitem_id).first()
    if favoriteitem_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai FavoriteItem jok")
    return favoriteitem_db


@favoriteitem_router.delete('/delete/{favoriteitem_id}')
async def delete_favoriteitem(favoriteitem_id: int, db: Session = Depends(get_db)):
    favoriteitem_db = db.query(FavoriteItem).filter(FavoriteItem.id == favoriteitem_id).first()
    if favoriteitem_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai FavoriteItem jok")
    db.delete(favoriteitem_db)
    db.commit()
    return {"message": "FavoriteItem deleted successfully"}

@favoriteitem_router.put('/update/{favoriteitem_id}')
async def update_favoriteitem(favoriteitem_id: int, favoriteitem_data: FavoriteItemShema, db: Session = Depends(get_db)):
    favoriteitem_db = db.query(FavoriteItem).filter(FavoriteItem.id == favoriteitem_id).first()
    if favoriteitem_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai FavoriteItem jok")
    favoriteitem_db.product_id = favoriteitem_data.product_id
    favoriteitem_db.user_id = favoriteitem_data.user_id
    db.commit()
    db.refresh(favoriteitem_db)
    return favoriteitem_db