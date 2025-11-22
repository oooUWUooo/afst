from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BorrowBase(BaseModel):
    book_id: int
    reader_id: int

class BorrowCreate(BorrowBase):
    pass

class BorrowReturn(BaseModel):
    book_id: int
    reader_id: int

class Borrow(BorrowBase):
    id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        from_attributes = True