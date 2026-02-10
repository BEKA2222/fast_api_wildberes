from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Favorite
from mysite.db.schema import FavoriteShema



favorite_router = APIRouter(prefix='/favorite', tags=['favorite'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@favorite_router.post('/create')
async def create_favorite(favorite_data: FavoriteShema, db: Session = Depends(get_db)):
    favorite_db = Favorite(**favorite_data.dict())
    db.add(favorite_db)
    db.commit()
    db.refresh(favorite_db)
    return favorite_db


@favorite_router.get('/get')
async def get_favorites(db: Session = Depends(get_db)):
    favorites_db = db.query(Favorite).all()
    return favorites_db

@favorite_router.get('/get/{favorite_id}')
async def detail_favorite(favorite_id: int, db: Session = Depends(get_db)):
    favorite_db = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if favorite_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Favorite jok")
    return favorite_db

@favorite_router.delete('/delete/{favorite_id}')
async def delete_favorite(favorite_id: int, db: Session = Depends(get_db)):
    favorite_db = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if favorite_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Favorite jok")
    db.delete(favorite_db)
    db.commit()
    return {"message": "Favorite deleted successfully"}


@favorite_router.put('/update/{favorite_id}')
async def update_favorite(favorite_id: int, favorite_data: FavoriteShema, db: Session = Depends(get_db)):
    favorite_db = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if favorite_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Favorite jok")
    favorite_db.product_id = favorite_data.product_id
    favorite_db.user_id = favorite_data.user_id
    db.commit()
    db.refresh(favorite_db)
    return favorite_db