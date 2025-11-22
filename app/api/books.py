from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth.jwt_handler import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Book])
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all books - can be public or protected based on requirements"""
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books

@router.get("/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID"""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=schemas.Book, dependencies=[Depends(get_current_active_user)])
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Create a new book - requires authentication"""
    # Check if ISBN already exists (if provided)
    if book.isbn:
        existing_book = db.query(models.Book).filter(models.Book.isbn == book.isbn).first()
        if existing_book:
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.put("/{book_id}", response_model=schemas.Book, dependencies=[Depends(get_current_active_user)])
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Update a book - requires authentication"""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if ISBN is being updated and if it already exists
    if book_update.isbn and book_update.isbn != db_book.isbn:
        existing_book = db.query(models.Book).filter(models.Book.isbn == book_update.isbn).first()
        if existing_book:
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    for field, value in book_update.model_dump(exclude_unset=True).items():
        setattr(db_book, field, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", dependencies=[Depends(get_current_active_user)])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book - requires authentication"""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if book is currently borrowed
    active_borrows = db.query(models.Borrow).filter(
        models.Borrow.book_id == book_id,
        models.Borrow.is_returned == False
    ).count()
    
    if active_borrows > 0:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete book that is currently borrowed"
        )
    
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}