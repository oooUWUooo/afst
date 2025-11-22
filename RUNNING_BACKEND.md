# Running the Example Backend

This document explains how to run the example backend server for the Library Management System frontend.

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Install the required packages:

```bash
pip install fastapi uvicorn python-multipart
```

Or if you prefer using a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install fastapi uvicorn python-multipart
```

## Running the Server

To start the backend server:

```bash
uvicorn example_backend:app --reload
```

The server will start on `http://localhost:8000` by default.

## Using with the Frontend

1. Start the backend server as described above
2. Open the frontend application in your browser (either locally or from GitHub Pages)
3. In the "API Configuration" section, enter the backend URL:
   - If running locally: `http://localhost:8000`
   - If running on a remote server: `https://your-server-domain.com`
4. Click "Save URL"
5. You can now register/login and use all the features of the Library Management System

## Testing the API

You can test the API endpoints directly by visiting:
- `http://localhost:8000/docs` - Interactive API documentation
- `http://localhost:8000/redoc` - Alternative API documentation

## Important Notes

⚠️ **This is a demonstration backend only**:
- Data is stored in memory and will be lost when the server restarts
- Passwords are stored in plain text (not secure for production)
- No proper authentication validation beyond basic tokens
- No rate limiting or security measures implemented

For production use, you should implement a proper backend with:
- Database storage (PostgreSQL, MySQL, etc.)
- Secure password hashing
- JWT token validation
- Proper error handling
- Rate limiting
- Input validation
- Security measures (CORS, CSRF protection, etc.)