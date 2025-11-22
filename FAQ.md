# Frequently Asked Questions (FAQ)

## Q: Why does the login fail with "NetworkError when attempting to fetch resource"?

**A**: This error occurs because the frontend application is trying to connect to a backend API server, but GitHub Pages is a static hosting service that cannot handle API requests directly. To fix this:

1. Deploy a backend server that implements the required API endpoints
2. Configure the API URL in the frontend application:
   - Go to your deployed GitHub Pages site
   - Find the "API Configuration" section
   - Enter your backend server URL (e.g., `https://your-backend.herokuapp.com`)
   - Click "Save URL"
3. Now you can register/login and use the application

## Q: Where can I find the backend implementation?

**A**: This repository contains only the frontend. You'll need to implement or deploy a backend server separately. An example backend implementation is provided in `example_backend.py` in this repository.

## Q: How do I deploy the frontend to GitHub Pages?

**A**: Follow these steps:

1. Push this code to a GitHub repository
2. Go to repository Settings → Pages
3. Select source as "Deploy from a branch"
4. Choose the `main` branch and `/` (root) folder (or `/docs` if you move files there)
5. Save settings and wait for deployment
6. The site will be available at `https://<username>.github.io/<repository-name>`

## Q: What are the required backend API endpoints?

**A**: Your backend must implement these endpoints:

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

## Q: Do I need to run the backend server locally?

**A**: You can run the backend server locally for development, but for the GitHub Pages frontend to access it, you need to either:

1. Run both frontend and backend on localhost (use the script in `start_server.py` for frontend)
2. Deploy the backend to a publicly accessible server and configure the URL in the frontend

## Q: How do I test the application locally?

**A**: You can test locally in two ways:

1. **Frontend only**: Run `python start_server.py` to start a local server for the frontend
2. **Full application**: 
   - Run the backend server: `uvicorn example_backend:app --reload`
   - Run the frontend server: `python start_server.py`
   - Configure the API URL in the frontend to point to your backend (e.g., `http://localhost:8000`)

## Q: What about CORS (Cross-Origin Resource Sharing)?

**A**: When running frontend and backend on different ports or domains, you need to configure CORS in your backend to allow requests from your frontend domain. For GitHub Pages, your backend should allow requests from `https://yourusername.github.io`.

## Q: Can I use this frontend without a backend?

**A**: The frontend will load and display the UI, but all interactive features (authentication, book management, etc.) require a backend API to function. You need to connect to a backend to use the full functionality.

## Q: Where are my credentials and API URL stored?

**A**: The application stores your API URL and authentication token in the browser's localStorage. This means:
- The settings persist between browser sessions
- They are specific to each browser/device
- Clearing browser data will remove these settings
- You'll need to reconfigure the API URL and log in again after clearing data

## Q: How do I reset the application settings?

**A**: To reset the API URL and clear authentication:
1. Open browser developer tools (F12)
2. Go to the Application/Storage tab
3. Find and clear the localStorage entries for the site
4. Refresh the page

## Q: What if I get a "Failed to fetch" error?

**A**: This usually means:
1. The backend server is not running
2. The configured API URL is incorrect
3. Network issues preventing connection
4. CORS issues if running on different domains/ports

Check that your backend is running and accessible, and that the API URL is correctly configured in the frontend.