from fastapi import FastAPI
from .api import auth, books, readers, borrows

app = FastAPI(title="Library Management API", version="1.0.0")

# Include API routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(readers.router, prefix="/readers", tags=["readers"])
app.include_router(borrows.router, prefix="/borrows", tags=["borrows"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Library Management API"}