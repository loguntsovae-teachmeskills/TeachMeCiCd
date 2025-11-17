# Быстрый запуск TeachMe CI/CD

## Запуск приложения

### Вариант 1: Локальный запуск (для разработки)

```bash
# 1. Создание виртуального окружения
python3 -m venv venv

# 2. Активация окружения
source venv/bin/activate  # macOS/Linux
# или
venv\Scripts\activate  # Windows

# 3. Установка зависимостей
pip install -r requirements.txt

# 4. Запуск приложения
python main.py
```

Приложение доступно: **http://localhost:8000**  
Документация API: **http://localhost:8000/docs**

### Вариант 2: Docker Compose (рекомендуется)

```bash
# Сборка и запуск
docker compose up -d --build

# Просмотр логов
docker compose logs -f

# Остановка
docker compose down
```

## Тестирование API

### Health Check
```bash
curl http://localhost:8000/health
```

### Создание пользователя
```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepass123",
    "full_name": "John Doe"
  }'
```

### Получение списка пользователей
```bash
curl http://localhost:8000/api/v1/users
```

### Поиск пользователя по username
```bash
curl http://localhost:8000/api/v1/users/search/by-username/johndoe
```

## Запуск тестов

```bash
# Все тесты
pytest

# С подробным выводом
pytest -v

# Только smoke тесты
pytest -m smoke

# С coverage
pytest --cov=. --cov-report=html
```

## Полезные команды

### Форматирование кода
```bash
black .
isort .
```

### Проверка кода
```bash
flake8 .
mypy .
```

### Остановка приложения
```bash
# Найти процесс
ps aux | grep "python main.py"

# Остановить по PID
kill <PID>

# Или остановить все Python процессы на порту 8000
lsof -ti:8000 | xargs kill -9
```

## CI/CD

После push в GitHub автоматически запустятся workflows:
- **CI** - тестирование и проверка качества
- **CD** - деплой (для ветки main)
- **Docker Test** - проверка Docker сборки

Статус workflows можно посмотреть во вкладке "Actions" на GitHub.
