from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from .. import models, schemas
from ..database import get_db
from ..auth.jwt_handler import get_current_active_user

router = APIRouter()

@router.post("/borrow", dependencies=[Depends(get_current_active_user)])
def borrow_book(borrow_data: schemas.BorrowCreate, db: Session = Depends(get_db)):
    """Borrow a book - requires authentication and implements business rules"""
    # Check if book exists and has available copies
    book = db.query(models.Book).filter(models.Book.id == borrow_data.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book.copies <= 0:
        raise HTTPException(status_code=400, detail="No available copies of this book")
    
    # Check if reader exists
    reader = db.query(models.Reader).filter(models.Reader.id == borrow_data.reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    # Check if reader already has 3 books borrowed
    active_borrows_count = db.query(models.Borrow).filter(
        models.Borrow.reader_id == borrow_data.reader_id,
        models.Borrow.is_returned == False
    ).count()
    
    if active_borrows_count >= 3:
        raise HTTPException(
            status_code=400, 
            detail="Reader cannot borrow more than 3 books simultaneously"
        )
    
    # Check if this specific book is already borrowed by this reader
    existing_borrow = db.query(models.Borrow).filter(
        models.Borrow.book_id == borrow_data.book_id,
        models.Borrow.reader_id == borrow_data.reader_id,
        models.Borrow.is_returned == False
    ).first()
    
    if existing_borrow:
        raise HTTPException(
            status_code=400,
            detail="This book is already borrowed by this reader"
        )
    
    # Create borrow record
    db_borrow = models.Borrow(
        book_id=borrow_data.book_id,
        reader_id=borrow_data.reader_id
    )
    db.add(db_borrow)
    
    # Decrease book copies
    book.copies -= 1
    
    db.commit()
    db.refresh(db_borrow)
    
    return {"message": "Book borrowed successfully", "borrow_id": db_borrow.id}


@router.post("/return", dependencies=[Depends(get_current_active_user)])
def return_book(return_data: schemas.BorrowReturn, db: Session = Depends(get_db)):
    """Return a book - requires authentication and implements business rules"""
    # Find the borrow record
    borrow_record = db.query(models.Borrow).filter(
        models.Borrow.book_id == return_data.book_id,
        models.Borrow.reader_id == return_data.reader_id,
        models.Borrow.is_returned == False
    ).first()
    
    if not borrow_record:
        raise HTTPException(
            status_code=400,
            detail="This book was not borrowed by this reader or already returned"
        )
    
    # Update the borrow record
    borrow_record.return_date = datetime.utcnow()
    borrow_record.is_returned = True
    
    # Increase book copies
    book = db.query(models.Book).filter(models.Book.id == return_data.book_id).first()
    if book:
        book.copies += 1
    
    db.commit()
    
    return {"message": "Book returned successfully"}


@router.get("/reader/{reader_id}/borrowed", response_model=List[schemas.Borrow])
def get_reader_borrowed_books(reader_id: int, db: Session = Depends(get_db)):
    """Get all books currently borrowed by a specific reader - requires authentication"""
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    borrowed_books = db.query(models.Borrow).filter(
        models.Borrow.reader_id == reader_id,
        models.Borrow.is_returned == False
    ).all()
    
    return borrowed_books


@router.get("/", response_model=List[schemas.Borrow])
def get_all_borrows(db: Session = Depends(get_db)):
    """Get all borrow records - requires authentication"""
    borrows = db.query(models.Borrow).all()
    return borrows