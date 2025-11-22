// Configuration file for API endpoints
// This allows easy customization for different environments

// Default configuration for local development
const config = {
    apiUrl: 'http://localhost:8000',  // Change this to your deployed backend URL
    
    // You can add other configuration options here as needed
    endpoints: {
        auth: {
            register: '/auth/register',
            login: '/auth/login'
        },
        books: {
            getAll: '/books/',
            getById: '/books/{id}',
            create: '/books/',
            update: '/books/{id}',
            delete: '/books/{id}'
        },
        readers: {
            getAll: '/readers/',
            getById: '/readers/{id}',
            create: '/readers/',
            update: '/readers/{id}',
            delete: '/readers/{id}'
        },
        borrows: {
            getAll: '/borrows/',
            borrow: '/borrows/borrow',
            return: '/borrows/return',
            getByReader: '/reader/{reader_id}/borrowed'
        }
    }
};

// For GitHub Pages deployment, you might want to use a different API URL
// Uncomment and modify the following for production:
/*
const config = {
    apiUrl: 'https://your-username.github.io/your-repo-name/api',  // Update to your actual backend URL
    // ... rest of the configuration
};
*/

// Export the configuration
if (typeof module !== 'undefined' && module.exports) {
    module.exports = config;
} else if (typeof window !== 'undefined') {
    window.AppConfig = config;
}