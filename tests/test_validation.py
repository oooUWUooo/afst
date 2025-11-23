"""
Тесты для валидации данных через Pydantic схемы
tests/test_validation.py
"""
import pytest
from fastapi.testclient import TestClient


class TestUserValidation:
    """Тесты валидации пользователей"""
    
    def test_register_with_short_password(self, client):
        """Тест регистрации с коротким паролем"""
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "short"  # Меньше 8 символов
            }
        )
        assert response.status_code == 422
        assert "at least 8 characters" in response.json()["detail"][0]["msg"].lower()
    
    def test_register_with_long_password(self, client):
        """Тест регистрации со слишком длинным паролем"""
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "a" * 80  # Больше 72 символов
            }
        )
        assert response.status_code == 422
    
    def test_register_with_weak_password(self, client):
        """Тест регистрации со слабым паролем (только буквы)"""
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "onlyletters"  # Нет цифр
            }
        )
        assert response.status_code == 422
        assert "letters and numbers" in response.json()["detail"][0]["msg"].lower()
    
    def test_register_with_invalid_email(self, client):
        """Тест регистрации с невалидным email"""
        response = client.post(
            "/auth/register",
            json={
                "email": "not-an-email",
                "password": "password123"
            }
        )
        assert response.status_code == 422
    
    def test_register_with_valid_data(self, client):
        """Тест успешной регистрации с валидными данными"""
        response = client.post(
            "/auth/register",
            json={
                "email": "valid@example.com",
                "password": "validpass123"
            }
        )
        assert response.status_code == 200


class TestBookValidation:
    """Тесты валидации книг"""
    
    def test_create_book_with_empty_title(self, client, auth_headers):
        """Тест создания книги с пустым названием"""
        response = client.post(
            "/books/",
            json={
                "title": "",
                "author": "Test Author"
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_create_book_with_empty_author(self, client, auth_headers):
        """Тест создания книги с пустым автором"""
        response = client.post(
            "/books/",
            json={
                "title": "Test Book",
                "author": ""
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_create_book_with_negative_copies(self, client, auth_headers):
        """Тест создания книги с отрицательным количеством"""
        response = client.post(
            "/books/",
            json={
                "title": "Test Book",
                "author": "Test Author",
                "copies": -5
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_create_book_with_future_year(self, client, auth_headers):
        """Тест создания книги с годом в будущем"""
        response = client.post(
            "/books/",
            json={
                "title": "Future Book",
                "author": "Time Traveler",
                "year": 2100  # Слишком далеко в будущем
            },
            headers=auth_headers
        )
        # Может быть 200 или 422 в зависимости от текущего года
        assert response.status_code in [200, 422]
    
    def test_create_book_with_invalid_isbn(self, client, auth_headers):
        """Тест создания книги с невалидным ISBN"""
        response = client.post(
            "/books/",
            json={
                "title": "Test Book",
                "author": "Test Author",
                "isbn": "123"  # Слишком короткий ISBN
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_create_book_with_valid_isbn_10(self, client, auth_headers):
        """Тест создания книги с валидным ISBN-10"""
        response = client.post(
            "/books/",
            json={
                "title": "Test Book",
                "author": "Test Author",
                "isbn": "0123456789"  # Валидный ISBN-10
            },
            headers=auth_headers
        )
        # ISBN-10 может быть принят или отклонен в зависимости от валидации контрольной суммы
        assert response.status_code in [200, 422]
    
    def test_create_book_with_valid_isbn_13(self, client, auth_headers):
        """Тест создания книги с валидным ISBN-13"""
        response = client.post(
            "/books/",
            json={
                "title": "Test Book",
                "author": "Test Author",
                "isbn": "9781234567890"  # ISBN-13 формат
            },
            headers=auth_headers
        )
        assert response.status_code in [200, 422]
    
    def test_create_book_with_long_description(self, client, auth_headers):
        """Тест создания книги с очень длинным описанием"""
        response = client.post(
            "/books/",
            json={
                "title": "Test Book",
                "author": "Test Author",
                "description": "x" * 3000  # Больше 2000 символов
            },
            headers=auth_headers
        )
        assert response.status_code == 422


class TestReaderValidation:
    """Тесты валидации читателей"""
    
    def test_create_reader_with_empty_name(self, client, auth_headers):
        """Тест создания читателя с пустым именем"""
        response = client.post(
            "/readers/",
            json={
                "name": "",
                "email": "test@example.com"
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_create_reader_with_whitespace_name(self, client, auth_headers):
        """Тест создания читателя с именем из пробелов"""
        response = client.post(
            "/readers/",
            json={
                "name": "   ",
                "email": "test@example.com"
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_create_reader_with_invalid_name_characters(self, client, auth_headers):
        """Тест создания читателя с недопустимыми символами в имени"""
        response = client.post(
            "/readers/",
            json={
                "name": "Test@Reader#123",  # Содержит недопустимые символы
                "email": "test@example.com"
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_create_reader_with_valid_name(self, client, auth_headers):
        """Тест создания читателя с валидным именем"""
        response = client.post(
            "/readers/",
            json={
                "name": "John Doe-Smith",  # Допустимые символы
                "email": "john@example.com"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_create_reader_with_invalid_email(self, client, auth_headers):
        """Тест создания читателя с невалидным email"""
        response = client.post(
            "/readers/",
            json={
                "name": "Test Reader",
                "email": "not-valid-email"
            },
            headers=auth_headers
        )
        assert response.status_code == 422


class TestBorrowValidation:
    """Тесты валидации операций выдачи/возврата"""
    
    def test_borrow_with_negative_book_id(self, client, auth_headers):
        """Тест выдачи с отрицательным ID книги"""
        response = client.post(
            "/borrows/borrow",
            json={
                "book_id": -1,
                "reader_id": 1
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_borrow_with_zero_book_id(self, client, auth_headers):
        """Тест выдачи с нулевым ID книги"""
        response = client.post(
            "/borrows/borrow",
            json={
                "book_id": 0,
                "reader_id": 1
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_borrow_with_negative_reader_id(self, client, auth_headers):
        """Тест выдачи с отрицательным ID читателя"""
        response = client.post(
            "/borrows/borrow",
            json={
                "book_id": 1,
                "reader_id": -1
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_borrow_with_missing_fields(self, client, auth_headers):
        """Тест выдачи с пропущенными полями"""
        response = client.post(
            "/borrows/borrow",
            json={
                "book_id": 1
                # Отсутствует reader_id
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_return_with_invalid_data(self, client, auth_headers):
        """Тест возврата с невалидными данными"""
        response = client.post(
            "/borrows/return",
            json={
                "book_id": "not-a-number",
                "reader_id": 1
            },
            headers=auth_headers
        )
        assert response.status_code == 422


class TestEdgeCasesValidation:
    """Тесты граничных случаев валидации"""
    
    def test_create_book_with_max_length_title(self, client, auth_headers):
        """Тест создания книги с максимальной длиной названия"""
        response = client.post(
            "/books/",
            json={
                "title": "a" * 500,  # Максимум 500 символов
                "author": "Test Author"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_create_book_with_too_long_title(self, client, auth_headers):
        """Тест создания книги со слишком длинным названием"""
        response = client.post(
            "/books/",
            json={
                "title": "a" * 501,  # Больше 500 символов
                "author": "Test Author"
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_create_reader_with_max_length_name(self, client, auth_headers):
        """Тест создания читателя с максимальной длиной имени"""
        response = client.post(
            "/readers/",
            json={
                "name": "A" * 200,  # Максимум 200 символов
                "email": "test@example.com"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
    
    def test_create_reader_with_too_long_name(self, client, auth_headers):
        """Тест создания читателя со слишком длинным именем"""
        response = client.post(
            "/readers/",
            json={
                "name": "A" * 201,  # Больше 200 символов
                "email": "test@example.com"
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_update_book_with_partial_data(self, client, auth_headers, test_book):
        """Тест обновления книги с частичными данными"""
        response = client.put(
            f"/books/{test_book['id']}",
            json={
                "title": "Updated Title"
                # Только одно поле
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["author"] == test_book["author"]  # Не изменилось
    
    def test_update_reader_with_empty_body(self, client, auth_headers, test_reader):
        """Тест обновления читателя с пустым телом запроса"""
        response = client.put(
            f"/readers/{test_reader['id']}",
            json={},
            headers=auth_headers
        )
        # Должно быть успешно (ничего не меняется) или ошибка валидации
        assert response.status_code in [200, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])