# Library Management System - GitHub Pages Demo

This is a frontend-only demo of the Library Management System that can be deployed on GitHub Pages. It connects to a backend API to provide full functionality for managing books, readers, and borrowing operations.

**⚠️ ВАЖНО: Для полноценной работы приложения требуется отдельный backend-сервер.**

## Quick Start

If you want to quickly test the application functionality:

1. **For immediate testing**: Follow the [Quick Start Guide](QUICK_START.md) to run both frontend and backend locally
2. **For deployment**: Deploy the frontend to GitHub Pages and backend to a separate server
3. **For beginners**: Follow the [Setup Instructions](SETUP_INSTRUCTIONS.md) for a step-by-step guide to get the system running quickly
4. **Для русскоязычных пользователей**: См. [Быстрый старт на русском языке](QUICK_START_RU.md) для подробных инструкций на русском языке

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

To test locally, you have multiple options:

### Option 1: Full Application (Recommended)
To run the complete application with both frontend and backend:

1. **Start the backend server**:
   ```bash
   # Install dependencies first
   pip install fastapi uvicorn python-multipart
   
   # Run the backend
   uvicorn example_backend:app --reload
   ```
   The backend will run on `http://localhost:8000`

2. **In a new terminal, start the frontend server**:
   ```bash
   python start_server.py
   ```
   The frontend will run on `http://localhost:8080`

3. **Configure the API URL**:
   - Open `http://localhost:8080` in your browser
   - Go to the "API Configuration" section
   - Enter `http://localhost:8000` as the API URL
   - Click "Save URL"
   - Now you can register/login and use all features

For detailed instructions, see [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md).

### Option 2: Frontend Only
If you only want to test the frontend interface:

```bash
python start_server.py
```

Then open `http://localhost:8080` in your browser.

> Note: The provided start_server.py script enables CORS headers which might be helpful during development.

## Backend Integration

This frontend is designed to work with a FastAPI backend that implements the Library Management System API. The backend should provide JWT-based authentication and implement all the endpoints referenced in the JavaScript code.

### Deploying a Backend Server

Since GitHub Pages is a static hosting service, you need to deploy your backend to a separate server. You can:

1. **Deploy to Render.com** - Follow the instructions in [DEPLOY_BACKEND.md](DEPLOY_BACKEND.md) for the easiest deployment option
2. **Use the example backend** - An example implementation is provided in `example_backend.py`
3. **Deploy elsewhere** - You can deploy to Heroku, Railway, AWS, or any other cloud platform

After deploying your backend, configure the API URL in the frontend application through the "API Configuration" section.

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

To use all features of this application, you need to run a backend server. Multiple options are available:

1. **For local development**: Follow the instructions in [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md) to run both frontend and backend locally
2. **For deployment**: Use [DEPLOY_BACKEND.md](DEPLOY_BACKEND.md) for instructions on deploying to Render.com or other platforms
3. **Example implementation**: An example backend is provided in `example_backend.py`
4. **Requirements**: Your backend must implement all the endpoints referenced in the JavaScript code

## Deployment

To deploy to GitHub Pages:

1. Push this code to a GitHub repository
2. Go to repository Settings → Pages
3. Select source as "GitHub Actions" or "Deploy from a branch"
4. Choose the `main` branch and `/docs` folder
5. Save settings and wait for deployment

The site will be available at `https://<username>.github.io/<repository-name>`.