# Деплой Backend на Render.com для тестирования функциональности

Поскольку GitHub Pages предоставляет только статический хостинг, вам нужно развернуть backend на отдельной платформе для полноценной работы приложения. Render.com - это отличный выбор для быстрого деплоя backend-приложений.

## Подготовка к деплою на Render.com

### Шаг 1: Создание файла Dockerfile

Создайте файл `Dockerfile` в корне проекта:

```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "example_backend:app", "--host", "0.0.0.0", "--port", "10000"]
```

### Шаг 2: Создание файла requirements.txt

Создайте файл `requirements.txt`:

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pydantic==2.5.0
```

### Шаг 3: Регистрация на Render.com

1. Перейдите на [https://render.com](https://render.com)
2. Нажмите "Sign Up" и зарегистрируйтесь с помощью GitHub аккаунта
3. Подключите свой GitHub аккаунт к Render

### Шаг 4: Создание Web Service на Render

1. Войдите в Render Dashboard
2. Нажмите "New +" → "Web Service"
3. Выберите ваш GitHub репозиторий
4. Настройте параметры:
   - Environment: `Docker`
   - Branch: `main`
   - Region: `Frankfurt` (или ближайший к вам)
   - Instance Type: `Free`
5. В разделе "Advanced" добавьте переменные окружения (если нужно):
   - PORT: 10000
6. Нажмите "Create Web Service"

### Шаг 5: Настройка CORS в backend

В файле `example_backend.py` убедитесь, что у вас настроена поддержка CORS. Если нет, добавьте:

```python
from fastapi.middleware.cors import CORSMiddleware

# Добавьте после создания app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Шаг 6: Использование вашего backend

После успешного деплоя вы получите URL в формате `https://your-project-name.onrender.com`. 

1. Откройте ваше приложение на GitHub Pages
2. В разделе "API Configuration" введите URL вашего backend (без слэша в конце)
3. Нажмите "Save URL"
4. Теперь вы можете регистрироваться и использовать все функции приложения

## Альтернативные способы деплоя backend

### Heroku (через GitHub)

1. Зарегистрируйтесь на [https://heroku.com](https://heroku.com)
2. Создайте новое приложение
3. Подключите ваш GitHub репозиторий
4. Включите автоматический деплой с ветки main
5. Убедитесь, что у вас есть файл `Procfile` с содержимым:
   ```
   web: uvicorn example_backend:app --host=0.0.0.0 --port=${PORT:-5000}
   ```

### Railway

1. Перейдите на [https://railway.app](https://railway.app)
2. Создайте новый проект
3. Выберите "Deploy from GitHub repo"
4. Выберите ваш репозиторий
5. Укажите команду запуска: `uvicorn example_backend:app --host=0.0.0.0 --port=$PORT`

## Важные замечания

⚠️ **Для тестирования функциональности**:
- Данные в демо-бэкенде хранятся в памяти и будут сброшены при перезапуске сервера
- Пароли хранятся в открытом виде (не подходит для продакшена)
- Нет аутентификации токенов (только для демонстрации)

Для полноценного использования рекомендуется:
- Использовать базу данных (PostgreSQL, MongoDB и т.д.)
- Реализовать безопасное хранение паролей
- Добавить валидацию токенов
- Настроить CORS для конкретных доменов

## Проверка работоспособности

После деплоя backend вы можете проверить его работоспособность:
- Откройте `https://your-app.onrender.com/docs` для интерактивной документации API
- Откройте `https://your-app.onrender.com/redoc` для альтернативной документации

Если документация API открывается, значит backend работает корректно, и вы можете использовать его URL в приложении.