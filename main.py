"""
Главный файл FastAPI приложения.
Точка входа в приложение с настройкой роутов и middleware.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.routes import health, users

# Создание экземпляра приложения
app = FastAPI(
    title="TeachMe CI/CD API",
    description="Демонстрационное FastAPI приложение для изучения CI/CD процессов",
    version="1.0.2",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(health.router, tags=["Health"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])

# Подключение статических файлов (UI)
app.mount("/ui", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
async def root():
    """Корневой endpoint."""
    return {
        "message": "Добро пожаловать в TeachMe CI/CD API!",
        "version": "1.0.2",
        "docs": "/docs",
        "ui": "/ui",
    }


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Обработчик для несуществующих маршрутов."""
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint не найден", "path": str(request.url)},
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Обработчик внутренних ошибок сервера."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера", "message": str(exc)},
    )


if __name__ == "__main__":
    # Запуск сервера для разработки
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
        reload=True,  # Автоматическая перезагрузка при изменении кода
        log_level="info",
    )
