# Library Management System - GitHub Pages Demo

This is a frontend-only demo of the Library Management System that can be deployed on GitHub Pages. It connects to a backend API to provide full functionality for managing books, readers, and borrowing operations.

## Features

- User authentication (register/login/logout)
- Book management (add, search, view books)
- Reader management (add, search, view readers)
- Borrow/return system
- Dashboard with statistics
- Responsive design using Bootstrap 5
- Modern UI with Font Awesome icons

## How to Use

1. Deploy this frontend to GitHub Pages
2. Configure the backend API URL using the API Configuration section
3. Register/login to access the full functionality
4. Use the various sections to manage your library

## API Endpoints Used

The frontend communicates with the backend using these endpoints:
- `/auth/register` - User registration
- `/auth/login` - User login
- `/books/` - Book management
- `/readers/` - Reader management
- `/borrows/borrow` - Borrow a book
- `/borrows/return` - Return a book
- `/borrows/reader/{reader_id}/borrowed` - Get borrowed books for a reader

## Configuration

The API URL can be configured and saved in the browser's localStorage. This allows the frontend to remember your backend URL between sessions.

## Local Development

To test locally, you have two options:

### Option 1: Using the provided script
Run the local server script included in this repository:
```bash
python start_server.py
```

Then open `http://localhost:8080` in your browser.

### Option 2: Using Python's built-in server
```bash
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

> Note: The provided start_server.py script enables CORS headers which might be helpful during development.

## Backend Integration

This frontend is designed to work with a FastAPI backend that implements the Library Management System API. The backend should provide JWT-based authentication and implement all the endpoints referenced in the JavaScript code.

## Troubleshooting

If you encounter the error "Login failed: NetworkError when attempting to fetch resource", please refer to the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) file for detailed instructions on how to resolve this issue.

You can also check our [FAQ.md](FAQ.md) for answers to frequently asked questions.

The most common cause is that GitHub Pages is a static hosting service and cannot handle API requests directly. You need to deploy a separate backend service and configure the API URL in the frontend application.

## Technologies Used

- HTML5
- CSS3 (with Bootstrap 5)
- JavaScript (ES6+)
- Font Awesome (icons)
- GitHub Pages (deployment)

## Running a Backend Server

To use all features of this application, you need to run a backend server. An example backend implementation is provided in `example_backend.py` with instructions in `RUNNING_BACKEND.md`.

## Deployment

To deploy to GitHub Pages:

1. Push this code to a GitHub repository
2. Go to repository Settings → Pages
3. Select source as "GitHub Actions" or "Deploy from a branch"
4. Choose the `main` branch and `/docs` folder
5. Save settings and wait for deployment

The site will be available at `https://<username>.github.io/<repository-name>`.