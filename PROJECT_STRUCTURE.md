# Структура проекта Library Management System

## Описание файлов

### Основные файлы:
- `index.html` - Главная страница приложения с полным интерфейсом системы управления библиотекой
- `404.html` - Страница ошибки 404 для GitHub Pages
- `example_backend.py` - Пример backend-сервера на FastAPI с полной реализацией API
- `start_server.py` - Скрипт для запуска локального сервера с поддержкой CORS

### Файлы конфигурации:
- `Dockerfile` - Файл для контейнеризации backend-сервера
- `requirements.txt` - Зависимости для backend (FastAPI, uvicorn и др.)
- `.github/workflows/pages.yml` - GitHub Actions workflow для деплоя на GitHub Pages

### Файлы документации:
- `README.md` - Основное описание проекта
- `SETUP_INSTRUCTIONS.md` - Пошаговые инструкции по настройке
- `QUICK_START.md` - Быстрый старт на английском языке
- `QUICK_START_RU.md` - Быстрый старт на русском языке
- `TROUBLESHOOTING.md` - Решение проблем и ошибок
- `FAQ.md` - Часто задаваемые вопросы
- `DEPLOY_BACKEND.md` - Инструкции по деплою backend
- `LOCAL_DEVELOPMENT.md` - Руководство по локальной разработке
- `PROJECT_STRUCTURE.md` - Этот файл

### Файлы настройки:
- `.gitignore` - Список файлов, исключаемых из репозитория

## Как работает система

### Frontend (GitHub Pages):
1. Загружается `index.html` с интерфейсом
2. Пользователь вводит URL backend в разделе "API Configuration"
3. Приложение сохраняет URL в localStorage
4. Все запросы к API отправляются на указанный backend

### Backend (отдельный сервер):
1. Должен реализовывать все необходимые API-эндпоинты
2. Должен поддерживать CORS для домена GitHub Pages
3. Обрабатывает аутентификацию, управление книгами, читателями и т.д.

## Необходимые API-эндпоинты

### Аутентификация:
- `POST /auth/register` - Регистрация пользователя
- `POST /auth/login` - Вход пользователя

### Управление книгами:
- `GET /books/` - Получить все книги
- `POST /books/` - Добавить книгу

### Управление читателями:
- `GET /readers/` - Получить всех читателей
- `POST /readers/` - Добавить читателя

### Выдача/возврат книг:
- `POST /borrows/borrow` - Выдать книгу
- `POST /borrows/return` - Вернуть книгу
- `GET /borrows/reader/{reader_id}/borrowed` - Книги, взятые читателем
- `GET /borrows/borrowed` - Все выданные книги

## Проблема "Login failed: NetworkError when attempting to fetch resource"

Эта ошибка означает, что приложение не может подключиться к backend-серверу. Для решения:
1. Задеплойте backend на отдельный сервер (например, Render.com)
2. Введите URL backend в разделе "API Configuration"
3. Нажмите "Save URL"
4. Теперь можно регистрироваться и входить в систему

## Пример backend

Файл `example_backend.py` содержит полную реализацию всех необходимых эндпоинтов и готов к деплою.