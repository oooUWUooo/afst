"""
Конфигурация pytest и общие фикстуры для всех тестов
tests/conftest.py
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app import models


# ============ ТЕСТОВАЯ БАЗА ДАННЫХ ============

# Используем in-memory SQLite для тестов
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Используем StaticPool для in-memory БД
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ============ ФИКСТУРЫ ============

@pytest.fixture(scope="function")
def db_session():
    """
    Создает чистую сессию базы данных для каждого теста
    """
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Очищаем таблицы после теста
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Создает тестового клиента FastAPI с переопределенной БД
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client):
    """
    Создает тестового пользователя
    """
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    return {
        "email": user_data["email"],
        "password": user_data["password"],
        "user_data": response.json()
    }


@pytest.fixture
def auth_token(client, test_user):
    """
    Получает JWT токен для тестового пользователя
    """
    login_response = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """
    Возвращает заголовки аутентификации с JWT токеном
    """
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def test_book(client, auth_headers):
    """
    Создает тестовую книгу
    """
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "year": 2023,
        "isbn": "9781234567890",
        "copies": 5,
        "description": "Test description"
    }
    response = client.post("/books/", json=book_data, headers=auth_headers)
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def test_reader(client, auth_headers):
    """
    Создает тестового читателя
    """
    reader_data = {
        "name": "Test Reader",
        "email": "reader@example.com"
    }
    response = client.post("/readers/", json=reader_data, headers=auth_headers)
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def multiple_books(client, auth_headers):
    """
    Создает несколько тестовых книг
    """
    books = []
    for i in range(5):
        book_data = {
            "title": f"Test Book {i+1}",
            "author": f"Test Author {i+1}",
            "isbn": f"978{i+1}{i+1}{i+1}{i+1}{i+1}{i+1}{i+1}{i+1}{i+1}{i+1}",
            "copies": 3
        }
        response = client.post("/books/", json=book_data, headers=auth_headers)
        assert response.status_code == 200
        books.append(response.json())
    return books


@pytest.fixture
def multiple_readers(client, auth_headers):
    """
    Создает несколько тестовых читателей
    """
    readers = []
    for i in range(3):
        reader_data = {
            "name": f"Test Reader {i+1}",
            "email": f"reader{i+1}@example.com"
        }
        response = client.post("/readers/", json=reader_data, headers=auth_headers)
        assert response.status_code == 200
        readers.append(response.json())
    return readers


@pytest.fixture
def borrowed_book(client, auth_headers, test_book, test_reader):
    """
    Создает запись о выдаче книги
    """
    borrow_data = {
        "book_id": test_book["id"],
        "reader_id": test_reader["id"]
    }
    response = client.post("/borrows/borrow", json=borrow_data, headers=auth_headers)
    assert response.status_code == 200
    return {
        "book": test_book,
        "reader": test_reader,
        "borrow_data": response.json()
    }


# ============ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ============

def create_book(client, auth_headers, **kwargs):
    """
    Вспомогательная функция для создания книги с кастомными параметрами
    """
    default_data = {
        "title": "Default Book",
        "author": "Default Author",
        "copies": 1
    }
    default_data.update(kwargs)
    
    response = client.post("/books/", json=default_data, headers=auth_headers)
    return response


def create_reader(client, auth_headers, **kwargs):
    """
    Вспомогательная функция для создания читателя с кастомными параметрами
    """
    default_data = {
        "name": "Default Reader",
        "email": "default@example.com"
    }
    default_data.update(kwargs)
    
    response = client.post("/readers/", json=default_data, headers=auth_headers)
    return response


def borrow_book(client, auth_headers, book_id, reader_id):
    """
    Вспомогательная функция для выдачи книги
    """
    borrow_data = {
        "book_id": book_id,
        "reader_id": reader_id
    }
    response = client.post("/borrows/borrow", json=borrow_data, headers=auth_headers)
    return response


def return_book(client, auth_headers, book_id, reader_id):
    """
    Вспомогательная функция для возврата книги
    """
    return_data = {
        "book_id": book_id,
        "reader_id": reader_id
    }
    response = client.post("/borrows/return", json=return_data, headers=auth_headers)
    return response


# ============ МАРКЕРЫ ============

def pytest_configure(config):
    """
    Регистрация кастомных маркеров pytest
    """
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "business_logic: marks tests that test business logic"
    )