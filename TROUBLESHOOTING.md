# Troubleshooting GitHub Pages Deployment

## Common Issues and Solutions

### 1. "Login failed: NetworkError when attempting to fetch resource"

This error occurs because the frontend application needs to connect to a backend API server, but GitHub Pages is a static hosting service that cannot handle API requests directly.

#### Solution:

1. **Deploy a Backend API Server**: You need to have a separate backend service that handles authentication and data operations. This can be:
   - A server running on a cloud platform (AWS, Google Cloud, Azure, etc.)
   - A service like Render, Heroku, or Railway
   - A self-hosted server
   - **For local testing**: Run the example backend locally (see below)

2. **Configure the API URL**:
   - After deploying your frontend to GitHub Pages
   - Access your deployed site
   - In the "API Configuration" section, enter the URL of your backend API
   - Click "Save URL"

3. **Local Backend for Testing**:
   - Install dependencies: `pip install fastapi uvicorn python-multipart`
   - Run the backend: `uvicorn example_backend:app --reload`
   - The backend will run on `http://localhost:8000`
   - Configure the frontend to use this URL

4. **Backend Requirements**:
   Your backend API must implement these endpoints:
   - `POST /auth/register` - User registration
   - `POST /auth/login` - User login
   - `GET /books/` - Get all books
   - `POST /books/` - Add a new book
   - `GET /readers/` - Get all readers
   - `POST /readers/` - Add a new reader
   - `POST /borrows/borrow` - Borrow a book
   - `POST /borrows/return` - Return a book
   - `GET /borrows/reader/{reader_id}/borrowed` - Get borrowed books for a reader
   - `GET /borrows/borrowed` - Get all borrowed books

5. **CORS Configuration**:
   Make sure your backend allows Cross-Origin Resource Sharing (CORS) from your GitHub Pages domain:
   ```
   Access-Control-Allow-Origin: https://yourusername.github.io
   ```

### 2. GitHub Pages Deployment

If your GitHub Pages site isn't loading properly:

1. Check that your repository settings have GitHub Pages enabled
2. Make sure the source is set to the correct branch (usually `main`)
3. Verify that the `/docs` folder or root directory contains your HTML files

### 3. Local Testing

To test locally before deploying:

```bash
# Navigate to the project directory
cd /path/to/your/project

# Start a local server
python -m http.server 8000

# Or use Node.js
npx serve .

# Then open http://localhost:8000 in your browser
```

### 4. API URL Configuration

The application saves your API URL in browser localStorage. If you need to change it:

1. Open browser developer tools (F12)
2. Go to Application/Storage tab
3. Clear the "apiUrl" entry from localStorage
4. Or use the API Configuration section in the app

## Example Backend Implementation

For testing purposes, you can create a simple backend using FastAPI:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import jwt
from datetime import datetime, timedelta

app = FastAPI()

# Example models
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

# Example endpoints
@app.post("/auth/login")
async def login(user: User):
    # Implement your authentication logic here
    return {"access_token": "fake_token_here", "token_type": "bearer"}

@app.get("/books/")
async def get_books():
    # Return a list of books
    return []

@app.post("/books/")
async def add_book(book: Book):
    # Add book logic here
    return book
```

## Security Note

⚠️ **Important**: Never expose sensitive information in client-side code. The authentication tokens are stored in browser localStorage, which is accessible to JavaScript. For production use, ensure proper security measures are in place.