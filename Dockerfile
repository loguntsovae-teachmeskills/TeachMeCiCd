# Используем официальный образ Python как базовый
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
# --no-cache-dir уменьшает размер образа
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения в контейнер
COPY . .

# Создаем непривилегированного пользователя для запуска приложения
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Переключаемся на непривилегированного пользователя
USER appuser

# Открываем порт 8000 для приложения
EXPOSE 8000

# Команда для запуска приложения
# Используем uvicorn напрямую для production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
