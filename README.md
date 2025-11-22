# Library Management System - Full Stack Application

This is a full-stack Library Management System with a FastAPI backend and a JavaScript frontend. The application allows users to manage books, readers, and book borrowing/returning operations.

## 🚀 Features

### Backend (FastAPI)
- User authentication (register/login with JWT)
- Book management (CRUD operations)
- Reader management (CRUD operations)
- Borrowing system with business rules:
  - Max 3 books per reader at a time
  - Validation for available copies
  - Prevent deletion of books currently borrowed
  - Track borrowing history

### Frontend (GitHub Pages Demo)
- User-friendly interface built with Bootstrap 5
- Complete CRUD operations for books and readers
- Borrow and return functionality
- Responsive design for all devices
- Secure authentication with JWT tokens

## 📁 Project Structure

```
/
├── app/                    # FastAPI backend application
│   ├── api/               # API routes
│   ├── auth/              # Authentication handlers
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── config.py          # Configuration
│   ├── database.py        # Database setup
│   └── main.py            # Main application
├── frontend/              # GitHub Pages frontend
│   ├── index.html         # Main frontend page
│   ├── script.js          # Frontend JavaScript
│   ├── config.js          # API configuration
│   └── README.md          # Frontend documentation
├── alembic/               # Database migrations
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## 🛠️ Backend Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up the database:
   ```bash
   alembic upgrade head
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## 🌐 GitHub Pages Demo Setup

The frontend is designed to work with GitHub Pages:

1. Fork this repository
2. Update the API URL in `frontend/config.js` to point to your deployed backend
3. Enable GitHub Pages in your repository settings:
   - Go to Settings → Pages
   - Select "Deploy from a branch"
   - Choose the main branch and `/ (root)` folder
4. Access your demo at `https://your-username.github.io/repository-name`

## 📊 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Books
- `GET /books/` - Get all books
- `GET /books/{id}` - Get specific book
- `POST /books/` - Create new book (requires auth)
- `PUT /books/{id}` - Update book (requires auth)
- `DELETE /books/{id}` - Delete book (requires auth)

### Readers
- `GET /readers/` - Get all readers
- `GET /readers/{id}` - Get specific reader
- `POST /readers/` - Create new reader (requires auth)
- `PUT /readers/{id}` - Update reader (requires auth)
- `DELETE /readers/{id}` - Delete reader (requires auth)

### Borrows
- `POST /borrows/borrow` - Borrow a book (requires auth)
- `POST /borrows/return` - Return a book (requires auth)
- `GET /borrows/` - Get all borrow records
- `GET /reader/{id}/borrowed` - Get books borrowed by a specific reader

## 🚀 Deployment

### Backend Deployment Options
- Deploy to Heroku, Railway, or any Python-compatible platform
- Containerize with Docker
- Deploy to cloud providers (AWS, GCP, Azure)

### Frontend Deployment
- GitHub Pages (as described above)
- Netlify, Vercel, or any static hosting service

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.