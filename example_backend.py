"""
Example backend implementation for the Library Management System frontend.

This is a minimal FastAPI example that demonstrates the required endpoints
for the frontend to work properly.

To run this example:
1. Install required packages: pip install fastapi uvicorn python-multipart
2. Run the server: uvicorn example_backend:app --reload
3. Access the API at http://localhost:8000
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import json
import uuid

app = FastAPI(title="Library Management System API", version="1.0.0")

# Simple in-memory storage for demonstration purposes
users_db: Dict[str, dict] = {}
books_db: Dict[int, dict] = {}
readers_db: Dict[int, dict] = {}
borrows_db: Dict[int, dict] = {}

# Initialize with some sample data
books_db[1] = {
    "id": 1,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "year": 1925,
    "isbn": "978-0-7432-7356-5",
    "copies": 3,
    "description": "A classic American novel set in the summer of 1922.",
    "available_copies": 3
}

readers_db[1] = {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
}

class User(BaseModel):
    email: str
    password: str

class Book(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    copies: int = 1
    description: Optional[str] = None

class Reader(BaseModel):
    name: str
    email: str

class BorrowRequest(BaseModel):
    book_id: int
    reader_id: int

@app.post("/auth/register")
async def register(user: User):
    """Register a new user"""
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already registered")
    
    # In a real application, you would hash the password
    users_db[user.email] = {
        "email": user.email,
        "password": user.password,  # In production, use password hashing
        "id": len(users_db) + 1
    }
    
    return {"message": "User registered successfully"}

@app.post("/auth/login")
async def login(user: User):
    """Login and return access token"""
    if user.email not in users_db or users_db[user.email]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # In a real application, you would generate a proper JWT token
    token = f"fake_token_for_{user.email}_{uuid.uuid4()}"
    
    return {"access_token": token, "token_type": "bearer"}

@app.get("/books/")
async def get_books():
    """Get all books"""
    return list(books_db.values())

@app.post("/books/")
async def add_book(book: Book):
    """Add a new book"""
    new_id = max(books_db.keys()) + 1 if books_db else 1
    books_db[new_id] = {
        "id": new_id,
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "copies": book.copies,
        "description": book.description,
        "available_copies": book.copies
    }
    return books_db[new_id]

@app.get("/readers/")
async def get_readers():
    """Get all readers"""
    return list(readers_db.values())

@app.post("/readers/")
async def add_reader(reader: Reader):
    """Add a new reader"""
    new_id = max(readers_db.keys()) + 1 if readers_db else 1
    readers_db[new_id] = {
        "id": new_id,
        "name": reader.name,
        "email": reader.email
    }
    return readers_db[new_id]

@app.post("/borrows/borrow")
async def borrow_book(request: BorrowRequest):
    """Borrow a book"""
    if request.book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if request.reader_id not in readers_db:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    book = books_db[request.book_id]
    if book["available_copies"] <= 0:
        raise HTTPException(status_code=400, detail="No available copies")
    
    # Update available copies
    book["available_copies"] -= 1
    
    # Create borrow record
    borrow_id = max(borrows_db.keys()) + 1 if borrows_db else 1
    borrow_record = {
        "id": borrow_id,
        "book_id": request.book_id,
        "reader_id": request.reader_id,
        "borrow_date": datetime.now().isoformat(),
        "return_date": None,
        "book": book  # Include book details for frontend
    }
    borrows_db[borrow_id] = borrow_record
    
    return {"message": "Book borrowed successfully", "borrow": borrow_record}

@app.post("/borrows/return")
async def return_book(request: BorrowRequest):
    """Return a book"""
    # Find active borrow record
    borrow_record = None
    for bid, borrow in borrows_db.items():
        if (borrow["book_id"] == request.book_id and 
            borrow["reader_id"] == request.reader_id and 
            borrow["return_date"] is None):
            borrow_record = borrow
            borrow_id = bid
            break
    
    if not borrow_record:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    
    # Update return date
    borrow_record["return_date"] = datetime.now().isoformat()
    
    # Update available copies
    book = books_db[request.book_id]
    book["available_copies"] += 1
    
    return {"message": "Book returned successfully", "borrow": borrow_record}

@app.get("/borrows/borrowed")
async def get_borrowed_books():
    """Get all currently borrowed books"""
    borrowed = []
    for borrow in borrows_db.values():
        if borrow["return_date"] is None:
            # Add book and reader details to the borrow record
            borrow_with_details = borrow.copy()
            if borrow["book_id"] in books_db:
                borrow_with_details["book"] = books_db[borrow["book_id"]]
            if borrow["reader_id"] in readers_db:
                borrow_with_details["reader"] = readers_db[borrow["reader_id"]]
            borrowed.append(borrow_with_details)
    return borrowed

@app.get("/borrows/reader/{reader_id}/borrowed")
async def get_reader_borrowed_books(reader_id: int):
    """Get borrowed books for a specific reader"""
    borrowed = []
    for borrow in borrows_db.values():
        if (borrow["reader_id"] == reader_id and 
            borrow["return_date"] is None):
            # Add book details to the borrow record
            borrow_with_details = borrow.copy()
            if borrow["book_id"] in books_db:
                borrow_with_details["book"] = books_db[borrow["book_id"]]
            borrowed.append(borrow_with_details)
    return borrowed

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)