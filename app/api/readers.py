from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..auth.jwt_handler import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Reader])
def get_readers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all readers - requires authentication"""
    readers = db.query(models.Reader).offset(skip).limit(limit).all()
    return readers

@router.get("/{reader_id}", response_model=schemas.Reader)
def get_reader(reader_id: int, db: Session = Depends(get_db)):
    """Get a specific reader by ID"""
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader

@router.post("/", response_model=schemas.Reader, dependencies=[Depends(get_current_active_user)])
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(get_db)):
    """Create a new reader - requires authentication"""
    # Check if email already exists
    existing_reader = db.query(models.Reader).filter(models.Reader.email == reader.email).first()
    if existing_reader:
        raise HTTPException(status_code=400, detail="Reader with this email already exists")
    
    db_reader = models.Reader(**reader.model_dump())
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader

@router.put("/{reader_id}", response_model=schemas.Reader, dependencies=[Depends(get_current_active_user)])
def update_reader(reader_id: int, reader_update: schemas.ReaderUpdate, db: Session = Depends(get_db)):
    """Update a reader - requires authentication"""
    db_reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not db_reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    # Check if email is being updated and if it already exists
    if reader_update.email and reader_update.email != db_reader.email:
        existing_reader = db.query(models.Reader).filter(models.Reader.email == reader_update.email).first()
        if existing_reader:
            raise HTTPException(status_code=400, detail="Reader with this email already exists")
    
    for field, value in reader_update.model_dump(exclude_unset=True).items():
        setattr(db_reader, field, value)
    
    db.commit()
    db.refresh(db_reader)
    return db_reader

@router.delete("/{reader_id}", dependencies=[Depends(get_current_active_user)])
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    """Delete a reader - requires authentication"""
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    # Check if reader has active borrows
    active_borrows = db.query(models.Borrow).filter(
        models.Borrow.reader_id == reader_id,
        models.Borrow.is_returned == False
    ).count()
    
    if active_borrows > 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete reader that has borrowed books"
        )
    
    db.delete(reader)
    db.commit()
    return {"message": "Reader deleted successfully"}