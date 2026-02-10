from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import Review
from mysite.db.schema import ReviewShema


review_router = APIRouter(prefix='/review', tags=['review'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@review_router.post('/create')
async def create_review(review_data: ReviewShema, db: Session = Depends(get_db)):
    new_review = Review(**review_data.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@review_router.get('/get')
async def get_reviews(db: Session = Depends(get_db)):
    reviews_db = db.query(Review).all()
    return reviews_db


@review_router.get('/get/{review_id}')
async def detail_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Review jok")
    return review_db


@review_router.delete('/delete/{review_id}')
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Review jok")
    db.delete(review_db)
    db.commit()
    return {"message": "Review deleted successfully"}


@review_router.put('/update/{review_id}')
async def update_review(review_id: int, review_data: ReviewShema, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Myndai Review jok")
    review_db.review_text = review_data.review_text
    db.commit()
    db.refresh(review_db)
    return review_db