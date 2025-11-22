from pydantic import BaseModel
from typing import Optional

class ReaderBase(BaseModel):
    name: str
    email: str

class ReaderCreate(ReaderBase):
    pass

class ReaderUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class Reader(ReaderBase):
    id: int

    class Config:
        from_attributes = True