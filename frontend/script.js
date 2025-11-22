// Configuration - uses config.js for API URL
const API_BASE_URL = window.AppConfig ? window.AppConfig.apiUrl : 'http://localhost:8000';

let authToken = null;
let currentUserEmail = null;

document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    const token = localStorage.getItem('authToken');
    const email = localStorage.getItem('userEmail');
    
    if (token && email) {
        authToken = token;
        currentUserEmail = email;
        showDashboard();
        loadDashboardData();
    } else {
        showLogin();
    }

    // Event listeners for login and registration
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('register-form').addEventListener('submit', handleRegister);
    document.getElementById('logout-btn').addEventListener('click', handleLogout);
    
    // Navigation
    document.querySelectorAll('.nav-link[data-section]').forEach(link => {
        link.addEventListener('click', function() {
            const sectionId = this.getAttribute('data-section');
            showSection(sectionId);
        });
    });
    
    // Modal buttons
    document.getElementById('save-book-btn').addEventListener('click', saveBook);
    document.getElementById('save-reader-btn').addEventListener('click', saveReader);
    document.getElementById('borrow-book-btn').addEventListener('click', borrowBook);
    document.getElementById('return-book-btn').addEventListener('click', returnBook);
    
    // Load initial data for modals
    loadBooksForModal();
    loadReadersForModal();
});

function showLogin() {
    document.getElementById('login-section').style.display = 'block';
    document.getElementById('dashboard-section').style.display = 'none';
}

function showDashboard() {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('dashboard-section').style.display = 'block';
    
    // Show default section
    showSection('books-section');
}

function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active-section');
        section.style.display = 'none';
    });
    
    // Show selected section
    const section = document.getElementById(sectionId);
    section.style.display = 'block';
    section.classList.add('active-section');
    
    // Load data for the section
    switch(sectionId) {
        case 'books-section':
            loadBooks();
            break;
        case 'readers-section':
            loadReaders();
            break;
        case 'borrows-section':
            loadBorrows();
            break;
        case 'profile-section':
            loadProfile();
            break;
    }
}

async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            authToken = data.access_token;
            currentUserEmail = email;
            
            // Store in localStorage
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('userEmail', currentUserEmail);
            
            showDashboard();
            loadDashboardData();
        } else {
            alert('Login failed: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed: ' + error.message);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Registration successful! You can now login.');
        } else {
            alert('Registration failed: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Registration failed: ' + error.message);
    }
}

function handleLogout() {
    authToken = null;
    currentUserEmail = null;
    
    // Clear localStorage
    localStorage.removeItem('authToken');
    localStorage.removeItem('userEmail');
    
    showLogin();
}

async function loadDashboardData() {
    await loadBooks();
    await loadReaders();
    await loadBorrows();
}

async function loadBooks() {
    try {
        const response = await fetch(`${API_BASE_URL}/books/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            const books = await response.json();
            displayBooks(books);
        } else {
            console.error('Failed to load books:', await response.text());
        }
    } catch (error) {
        console.error('Error loading books:', error);
    }
}

function displayBooks(books) {
    const tbody = document.querySelector('#books-table tbody');
    tbody.innerHTML = '';
    
    books.forEach(book => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${book.id}</td>
            <td>${book.title}</td>
            <td>${book.author}</td>
            <td>${book.year || ''}</td>
            <td>${book.isbn || ''}</td>
            <td>${book.copies}</td>
            <td>${book.description || ''}</td>
            <td>
                <button class="btn btn-sm btn-warning me-1" onclick="editBook(${book.id})">Edit</button>
                <button class="btn btn-sm btn-danger" onclick="deleteBook(${book.id})">Delete</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function saveBook() {
    const title = document.getElementById('book-title').value;
    const author = document.getElementById('book-author').value;
    const year = document.getElementById('book-year').value || null;
    const isbn = document.getElementById('book-isbn').value || null;
    const copies = parseInt(document.getElementById('book-copies').value);
    const description = document.getElementById('book-description').value || null;
    
    const bookData = {
        title,
        author,
        copies,
        description
    };
    
    if (year) bookData.year = year;
    if (isbn) bookData.isbn = isbn;
    
    try {
        const response = await fetch(`${API_BASE_URL}/books/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(bookData)
        });
        
        if (response.ok) {
            document.getElementById('addBookModal').querySelector('.btn-close').click();
            loadBooks();
            document.getElementById('add-book-form').reset();
        } else {
            const error = await response.json();
            alert('Failed to save book: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error saving book:', error);
        alert('Error saving book: ' + error.message);
    }
}

async function deleteBook(id) {
    if (!confirm('Are you sure you want to delete this book?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/books/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            loadBooks();
        } else {
            const error = await response.json();
            alert('Failed to delete book: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error deleting book:', error);
        alert('Error deleting book: ' + error.message);
    }
}

async function loadReaders() {
    try {
        const response = await fetch(`${API_BASE_URL}/readers/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            const readers = await response.json();
            displayReaders(readers);
        } else {
            console.error('Failed to load readers:', await response.text());
        }
    } catch (error) {
        console.error('Error loading readers:', error);
    }
}

function displayReaders(readers) {
    const tbody = document.querySelector('#readers-table tbody');
    tbody.innerHTML = '';
    
    readers.forEach(reader => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${reader.id}</td>
            <td>${reader.name}</td>
            <td>${reader.email}</td>
            <td>
                <button class="btn btn-sm btn-warning me-1" onclick="editReader(${reader.id})">Edit</button>
                <button class="btn btn-sm btn-danger" onclick="deleteReader(${reader.id})">Delete</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function saveReader() {
    const name = document.getElementById('reader-name').value;
    const email = document.getElementById('reader-email').value;
    
    const readerData = {
        name,
        email
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/readers/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(readerData)
        });
        
        if (response.ok) {
            document.getElementById('addReaderModal').querySelector('.btn-close').click();
            loadReaders();
            document.getElementById('add-reader-form').reset();
        } else {
            const error = await response.json();
            alert('Failed to save reader: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error saving reader:', error);
        alert('Error saving reader: ' + error.message);
    }
}

async function deleteReader(id) {
    if (!confirm('Are you sure you want to delete this reader?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/readers/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            loadReaders();
        } else {
            const error = await response.json();
            alert('Failed to delete reader: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error deleting reader:', error);
        alert('Error deleting reader: ' + error.message);
    }
}

async function loadBorrows() {
    try {
        const response = await fetch(`${API_BASE_URL}/borrows/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            const borrows = await response.json();
            displayBorrows(borrows);
        } else {
            console.error('Failed to load borrows:', await response.text());
        }
    } catch (error) {
        console.error('Error loading borrows:', error);
    }
}

function displayBorrows(borrows) {
    const tbody = document.querySelector('#borrows-table tbody');
    tbody.innerHTML = '';
    
    borrows.forEach(borrow => {
        const borrowDate = new Date(borrow.borrow_date).toLocaleDateString();
        const returnDate = borrow.return_date ? new Date(borrow.return_date).toLocaleDateString() : 'Not returned';
        const status = borrow.is_returned ? 'Returned' : 'Borrowed';
        const statusClass = borrow.is_returned ? 'badge bg-success' : 'badge bg-warning';
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${borrow.id}</td>
            <td>${borrow.book ? borrow.book.title : 'N/A'}</td>
            <td>${borrow.reader ? borrow.reader.name : 'N/A'}</td>
            <td>${borrowDate}</td>
            <td>${returnDate}</td>
            <td><span class="${statusClass}">${status}</span></td>
            <td>
                ${!borrow.is_returned ? `<button class="btn btn-sm btn-success me-1" onclick="showReturnModal(${borrow.book.id}, ${borrow.reader.id})">Return</button>` : ''}
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function borrowBook() {
    const bookId = document.getElementById('borrow-book-id').value;
    const readerId = document.getElementById('borrow-reader-id').value;
    
    if (!bookId || !readerId) {
        alert('Please select both a book and a reader');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/borrows/borrow`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                book_id: parseInt(bookId),
                reader_id: parseInt(readerId)
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('borrowBookModal').querySelector('.btn-close').click();
            loadBorrows();
            loadBooks(); // Refresh books to show updated copies
            alert('Book borrowed successfully!');
        } else {
            alert('Failed to borrow book: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error borrowing book:', error);
        alert('Error borrowing book: ' + error.message);
    }
}

async function returnBook() {
    const bookId = document.getElementById('return-book-id').value;
    const readerId = document.getElementById('return-reader-id').value;
    
    if (!bookId || !readerId) {
        alert('Please select both a book and a reader');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/borrows/return`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                book_id: parseInt(bookId),
                reader_id: parseInt(readerId)
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('returnBookModal').querySelector('.btn-close').click();
            loadBorrows();
            loadBooks(); // Refresh books to show updated copies
            alert('Book returned successfully!');
        } else {
            alert('Failed to return book: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error returning book:', error);
        alert('Error returning book: ' + error.message);
    }
}

function showReturnModal(bookId, readerId) {
    // Populate the return modal with the selected book and reader
    document.getElementById('return-book-id').value = bookId;
    document.getElementById('return-reader-id').value = readerId;
    
    // Show the modal
    const modalElement = document.getElementById('returnBookModal');
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
}

async function loadBooksForModal() {
    try {
        const response = await fetch(`${API_BASE_URL}/books/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            const books = await response.json();
            populateBooksSelect(books);
        }
    } catch (error) {
        console.error('Error loading books for modal:', error);
    }
}

function populateBooksSelect(books) {
    const bookSelect = document.getElementById('borrow-book-id');
    const returnBookSelect = document.getElementById('return-book-id');
    
    // Clear existing options
    bookSelect.innerHTML = '<option value="">Select a book</option>';
    returnBookSelect.innerHTML = '<option value="">Select a book</option>';
    
    books.forEach(book => {
        if (book.copies > 0) { // Only show books with available copies for borrowing
            const option = document.createElement('option');
            option.value = book.id;
            option.textContent = `${book.title} by ${book.author}`;
            bookSelect.appendChild(option);
        }
        
        // For return, show all books
        const returnOption = document.createElement('option');
        returnOption.value = book.id;
        returnOption.textContent = `${book.title} by ${book.author}`;
        returnBookSelect.appendChild(returnOption);
    });
}

async function loadReadersForModal() {
    try {
        const response = await fetch(`${API_BASE_URL}/readers/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            const readers = await response.json();
            populateReadersSelect(readers);
        }
    } catch (error) {
        console.error('Error loading readers for modal:', error);
    }
}

function populateReadersSelect(readers) {
    const readerSelect = document.getElementById('borrow-reader-id');
    const returnReaderSelect = document.getElementById('return-reader-id');
    
    // Clear existing options
    readerSelect.innerHTML = '<option value="">Select a reader</option>';
    returnReaderSelect.innerHTML = '<option value="">Select a reader</option>';
    
    readers.forEach(reader => {
        const option = document.createElement('option');
        option.value = reader.id;
        option.textContent = `${reader.name} (${reader.email})`;
        readerSelect.appendChild(option);
        
        const returnOption = document.createElement('option');
        returnOption.value = reader.id;
        returnOption.textContent = `${reader.name} (${reader.email})`;
        returnReaderSelect.appendChild(returnOption);
    });
}

async function loadProfile() {
    document.getElementById('profile-email').textContent = currentUserEmail;
    
    // Try to get user's borrowed books
    try {
        // We need to find the reader ID for the current user first
        // For demo purposes, we'll just show a placeholder
        document.getElementById('my-borrows-list').innerHTML = '<p>This feature would show books borrowed by the current user.</p>';
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

// Edit functions (would need to be implemented)
function editBook(id) {
    alert('Edit functionality would be implemented here for book ID: ' + id);
}

function editReader(id) {
    alert('Edit functionality would be implemented here for reader ID: ' + id);
}