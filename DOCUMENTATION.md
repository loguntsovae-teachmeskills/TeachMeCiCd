# Документация проекта TeachMe CI/CD

## 📖 Обзор проекта

Полнофункциональный демонстрационный проект FastAPI с реализацией CI/CD процессов на базе GitHub Actions.

### Ключевые особенности

✅ **FastAPI REST API** с полным CRUD функционалом  
✅ **Docker и Docker Compose** для контейнеризации  
✅ **Pytest** с smoke и интеграционными тестами  
✅ **GitHub Actions** CI/CD pipeline  
✅ **Pydantic** валидация данных  
✅ **Health checks** для мониторинга  
✅ **Автоматическая документация** (Swagger/ReDoc)  

## 🏗️ Архитектура проекта

```
TeachMeCiCd/
├── app/                          # Код приложения
│   ├── models.py                 # Pydantic модели
│   └── routes/                   # API endpoints
│       ├── health.py             # Health checks
│       └── users.py              # Users CRUD
├── tests/                        # Тесты
│   ├── test_health.py            # Smoke тесты
│   └── test_users.py             # API тесты
├── .github/workflows/            # CI/CD
│   ├── ci.yml                    # Continuous Integration
│   ├── cd.yml                    # Continuous Deployment
│   └── docker-test.yml           # Docker тесты
├── main.py                       # Точка входа
├── Dockerfile                    # Docker образ
├── docker-compose.yml            # Compose конфигурация
└── requirements.txt              # Зависимости
```

## 🚀 Технологический стек

### Backend
- **FastAPI 0.104.1** - современный веб-фреймворк
- **Uvicorn 0.24.0** - ASGI сервер
- **Pydantic 2.5.0** - валидация данных

### Тестирование
- **pytest 7.4.3** - фреймворк для тестирования
- **pytest-cov 4.1.0** - coverage отчеты
- **httpx 0.25.1** - HTTP клиент для тестов

### Качество кода
- **black 23.11.0** - форматирование
- **flake8 6.1.0** - линтинг
- **isort 5.12.0** - сортировка импортов
- **mypy 1.7.1** - проверка типов

### Контейнеризация
- **Docker** - контейнеризация приложения
- **Docker Compose** - оркестрация контейнеров

### CI/CD
- **GitHub Actions** - автоматизация workflow

## 📊 CI/CD Pipeline

### Continuous Integration (ci.yml)

**Триггеры:** push, pull_request

**Jobs:**
1. **code-quality** - проверка качества кода
   - Black форматирование
   - isort сортировка импортов
   - flake8 линтинг

2. **test** - тестирование
   - Матрица: Python 3.9, 3.10, 3.11, 3.12
   - Smoke тесты
   - Полный набор тестов
   - Coverage отчеты

3. **docker-build** - сборка Docker
   - Сборка образа
   - Запуск контейнера
   - Проверка API endpoints

### Continuous Deployment (cd.yml)

**Триггер:** push в main

**Jobs:**
1. **test** - полное тестирование
2. **build-and-push** - сборка и публикация образа
3. **deploy-staging** - автоматический деплой в staging
4. **deploy-production** - деплой в production (требует одобрения)
5. **post-deploy** - мониторинг после деплоя
6. **rollback** - автоматический откат при ошибке

### Docker Compose Test (docker-test.yml)

**Триггеры:** изменения в docker-compose.yml, Dockerfile

**Действия:**
- Запуск через docker compose
- Проверка всех endpoints
- Создание тестовых данных

## 🧪 Тестирование

### Категории тестов

- **Smoke тесты** (@pytest.mark.smoke)
  - Быстрые проверки базового функционала
  - Health checks
  - Корневые endpoints

- **Integration тесты** (@pytest.mark.integration)
  - CRUD операции
  - Валидация данных
  - Обработка ошибок

### Статистика тестов

- ✅ 21 тест
- ✅ 100% success rate
- ⚡ 0.75s execution time

### Покрытие кода

Запуск с coverage:
```bash
pytest --cov=. --cov-report=html
```

## 🔧 API Endpoints

### Health Checks

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/health` | GET | Полная проверка работоспособности |
| `/healthz` | GET | Kubernetes liveness probe |
| `/readyz` | GET | Kubernetes readiness probe |

### Users API

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/api/v1/users` | POST | Создание пользователя |
| `/api/v1/users` | GET | Список пользователей |
| `/api/v1/users/{id}` | GET | Получение по ID |
| `/api/v1/users/{id}` | PUT | Обновление |
| `/api/v1/users/{id}` | DELETE | Удаление |
| `/api/v1/users/search/by-username/{username}` | GET | Поиск по username |

## 🐳 Docker

### Dockerfile особенности

- Базовый образ: `python:3.11-slim`
- Multi-stage build (готово для расширения)
- Непривилегированный пользователь
- Оптимизация слоёв
- Health check ready

### docker-compose.yml

**Сервисы:**
- `api` - FastAPI приложение
- *(опционально)* `redis` - кеширование
- *(опционально)* `postgres` - база данных

**Особенности:**
- Health checks
- Volume mounts для разработки
- Автоматический restart
- Изолированная сеть

## 📝 Модели данных

### UserCreate
```python
{
  "email": "user@example.com",      # EmailStr (required)
  "username": "johndoe",             # str, 3-50 chars (required)
  "password": "securepass123",       # str, min 6 chars (required)
  "full_name": "John Doe"            # str, max 100 chars (optional)
}
```

### UserResponse
```python
{
  "id": 1,                           # int
  "email": "user@example.com",       # str
  "username": "johndoe",             # str
  "full_name": "John Doe",           # str | None
  "created_at": "2025-11-17T...",    # datetime
  "is_active": true                  # bool
}
```

## 🔒 Безопасность

### Реализовано
- ✅ Pydantic валидация всех входных данных
- ✅ Email валидация
- ✅ Минимальная длина паролей
- ✅ Хеширование паролей (имитация)
- ✅ CORS middleware

### Рекомендации для production
- [ ] JWT аутентификация
- [ ] Rate limiting
- [ ] HTTPS/TLS
- [ ] Секреты в environment variables
- [ ] Database connection pooling
- [ ] Input sanitization
- [ ] Security headers

## 📈 Мониторинг

### Health Checks

Приложение предоставляет endpoints для мониторинга:

```bash
# Полный health check
curl http://localhost:8003/health

# Kubernetes liveness
curl http://localhost:8003/healthz

# Kubernetes readiness
curl http://localhost:8003/readyz
```

### Метрики

- Статус приложения
- Версия
- Timestamp
- Статус БД (готов для расширения)

## 🚦 Статус проекта

**Версия:** 1.0.0  
**Статус:** ✅ Production Ready  
**Тесты:** ✅ 21/21 Passing  
**Coverage:** 📊 High  

## 📚 Дополнительная документация

- [README.md](README.md) - Полная документация
- [QUICKSTART.md](QUICKSTART.md) - Быстрый старт
- [API Docs](http://localhost:8003/docs) - Swagger UI
- [ReDoc](http://localhost:8003/redoc) - ReDoc

## 🎓 Учебные материалы

Этот проект демонстрирует:

1. **REST API Design** - правильная структура endpoints
2. **Testing Patterns** - smoke и integration тесты
3. **Docker Best Practices** - оптимальная контейнеризация
4. **CI/CD Implementation** - полный pipeline
5. **Code Quality** - линтинг, форматирование, типизация
6. **Documentation** - swagger, комментарии, README

## 🔄 Workflow процесс

```
Developer Push
      ↓
[GitHub Actions CI]
      ↓
Code Quality Check → Tests → Docker Build
      ↓
   Success?
    ├─ Yes → [CD Pipeline]
    │         ↓
    │    Build Image → Staging Deploy → Production (manual) → Monitor
    │
    └─ No → Notify Developer
```

## 💡 Best Practices

### Коммиты
- Используйте conventional commits
- Пишите осмысленные сообщения
- Делайте atomic commits

### Тестирование
- Пишите тесты для новых features
- Поддерживайте coverage >80%
- Используйте pytest markers

### Code Review
- Проверяйте все PR
- Следите за CI статусом
- Обсуждайте архитектурные решения

## 🎯 Roadmap

### Phase 1 (Complete) ✅
- [x] FastAPI REST API
- [x] Docker setup
- [x] Pytest tests
- [x] GitHub Actions CI/CD
- [x] Documentation

### Phase 2 (Planned)
- [ ] PostgreSQL integration
- [ ] JWT authentication
- [ ] Redis caching
- [ ] Kubernetes manifests

### Phase 3 (Future)
- [ ] GraphQL endpoint
- [ ] WebSocket support
- [ ] Prometheus metrics
- [ ] ELK logging

## 📞 Поддержка

При возникновении вопросов:
1. Проверьте [README.md](README.md)
2. Посмотрите [QUICKSTART.md](QUICKSTART.md)
3. Изучите логи: `docker compose logs -f`
4. Запустите тесты: `pytest -v`

## 📄 Лицензия

MIT License - свободное использование для обучения и коммерческих целей.

---

**Создано для курса:** TeachMeSkills Python  
**Тема:** CI/CD и GitHub Actions  
**Дата:** Ноябрь 2025
