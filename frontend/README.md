# Library Management System - Frontend

This is a frontend application for the Library Management System that connects to a FastAPI backend. It provides a user-friendly interface to manage books, readers, and book borrowing/returning operations.

## Features

- User authentication (login/register)
- Manage books (add, view, edit, delete)
- Manage readers (add, view, edit, delete) 
- Borrow and return books
- View borrowing history
- Responsive design using Bootstrap

## Setup for GitHub Pages

### 1. Fork or clone this repository

### 2. Update the API base URL

In `script.js`, update the `API_BASE_URL` constant to point to your deployed backend:

```javascript
const API_BASE_URL = 'https://your-deployed-backend-url.com'; // Update this to your actual backend URL
```

### 3. Deploy to GitHub Pages

1. Go to your repository settings
2. Scroll down to the "GitHub Pages" section
3. Under "Source", select "Deploy from a branch"
4. Select the `main` branch and `/ (root)` folder
5. Click "Save"

Your frontend will be available at: `https://your-username.github.io/repository-name`

## Backend Connection

This frontend connects to a FastAPI backend that provides the following endpoints:

- `/auth/register` - User registration
- `/auth/login` - User authentication
- `/books/` - Book management
- `/readers/` - Reader management  
- `/borrows/` - Borrowing operations

## Functionality

### Authentication
- Register new users
- Login with existing credentials
- Automatic token storage in localStorage

### Books Management
- View all books with details
- Add new books with title, author, year, ISBN, etc.
- Edit existing book information
- Delete books (with validation)

### Readers Management
- View all registered readers
- Add new readers with name and email
- Edit reader information
- Delete readers (with validation)

### Borrowing System
- Borrow books with validation (max 3 books per reader)
- Return books with automatic inventory update
- View borrowing history
- Track return status

## Configuration

Before deploying, make sure to update the `API_BASE_URL` in `script.js` to match your deployed backend URL.

## Development

To run locally for development:
1. Open `index.html` in a web browser
2. Make sure your backend is running and accessible from the frontend
3. Update `API_BASE_URL` in `script.js` to your local backend URL (e.g., `http://localhost:8000`)

## Technologies Used

- HTML5
- CSS3 (with Bootstrap 5)
- JavaScript (ES6+)
- Bootstrap 5 for responsive UI
- Fetch API for HTTP requests
- JWT for authentication

## Security Notes

- Authentication tokens are stored in browser localStorage
- All API calls are secured with JWT tokens
- Input validation is performed on the backend