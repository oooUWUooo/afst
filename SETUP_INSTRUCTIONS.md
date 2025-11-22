# Быстрый запуск Library Management System

## Проблема: "Login failed: NetworkError when attempting to fetch resource"

Эта ошибка возникает, потому что GitHub Pages - это статический хостинг, который не может обрабатывать API-запросы. Приложению нужен отдельный backend-сервер для аутентификации и управления данными.

## Решение: Быстрый запуск готового backend

### Вариант 1: Деплой на Render.com (рекомендуется)

1. **Создайте аккаунт на [Render.com](https://render.com)**

2. **Создайте репозиторий на GitHub** с содержимым этого проекта

3. **Создайте Web Service на Render:**
   - Войдите в [Render Dashboard](https://dashboard.render.com)
   - Нажмите "New +" → "Web Service"
   - Выберите ваш GitHub репозиторий
   - Укажите:
     - Environment: `Docker`
     - Branch: `main`
     - Region: `Frankfurt` (или ближайший к вам)
     - Instance Type: `Free`
   - Нажмите "Create Web Service"

4. **После деплоя скопируйте URL** в формате `https://your-project-name.onrender.com`

### Вариант 2: Локальный запуск для тестирования

1. **Установите зависимости:**
   ```bash
   pip install fastapi uvicorn python-multipart
   ```

2. **Запустите backend:**
   ```bash
   uvicorn example_backend:app --reload
   ```

3. **Запустите frontend (в другом терминале):**
   ```bash
   python start_server.py
   ```

4. **Откройте `http://localhost:8080` в браузере**

5. **В разделе "API Configuration" введите `http://localhost:8000`**

## Настройка приложения

После деплоя или локального запуска:

1. **Введите URL вашего backend** в разделе "API Configuration"
2. **Нажмите "Save URL"**
3. **Зарегистрируйтесь** с помощью формы "Register"
4. **Войдите в систему** с помощью формы "Login"
5. **Используйте все функции приложения**

## Тестовые данные

После регистрации и входа в систему вы можете использовать следующие функции:

- **Добавление книг**: Используйте форму "Add New Book"
- **Добавление читателей**: Используйте форму "Add New Reader"
- **Выдача книг**: Используйте форму "Borrow a Book"
- **Возврат книг**: Используйте форму "Return a Book"

## Устранение проблем

Если вы все еще видите ошибку "Login failed: NetworkError when attempting to fetch resource":

1. **Проверьте URL backend** - убедитесь, что вы ввели правильный URL
2. **Проверьте работоспособность backend** - откройте `https://your-project-name.onrender.com/docs` для проверки
3. **Проверьте CORS настройки** - backend должен разрешать запросы с вашего домена
4. **Очистите localStorage** браузера и введите URL снова

## Примеры URL

- **GitHub Pages**: `https://yourusername.github.io/your-repo-name`
- **Render backend**: `https://your-project-name.onrender.com`
- **Локальный backend**: `http://localhost:8000`
- **Локальный frontend**: `http://localhost:8080`

## Готовые примеры

Backend уже настроен с примерами данных:
- Книга: "The Great Gatsby" (ID: 1)
- Читатель: "John Doe" (ID: 1)

После настройки API URL вы сможете использовать все функции системы управления библиотекой.