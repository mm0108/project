from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, crud
from database import get_db

router = APIRouter(prefix="/library")

@router.post("/books")
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)

@router.get("/books")
def get_books(db: Session = Depends(get_db)):
    return crud.get_books(db)

@router.post("/loan/{book_id}")
def loan(book_id: int, user: str, db: Session = Depends(get_db)):
    return crud.loan_book(db, book_id, user)

@router.post("/return/{book_id}")
def return_book(book_id: int, db: Session = Depends(get_db)):
    return crud.return_book(db, book_id)
