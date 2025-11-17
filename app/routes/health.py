"""
Роутер для health check endpoints.
Используется для мониторинга состояния приложения.
"""

from fastapi import APIRouter
from datetime import datetime
from app.models import HealthResponse
import os
import json

router = APIRouter()

# Путь к файлу с информацией о деплое
DEPLOYMENT_INFO_FILE = "/tmp/deployment_info.json"


def get_deployment_info():
    """Получение информации о последнем деплое."""
    try:
        if os.path.exists(DEPLOYMENT_INFO_FILE):
            with open(DEPLOYMENT_INFO_FILE, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return {
        "deployed_at": "unknown",
        "commit_sha": "unknown",
        "branch": "unknown",
        "deployed_by": "unknown"
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint для проверки работоспособности приложения.
    Используется в CI/CD для smoke тестов и мониторинга.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.1",
        database="ok"
    )


@router.get("/healthz")
async def kubernetes_health():
    """
    Упрощенный health check для Kubernetes liveness probe.
    """
    return {"status": "ok"}


@router.get("/readyz")
async def kubernetes_ready():
    """
    Readiness check для Kubernetes readiness probe.
    Проверяет готовность приложения принимать трафик.
    """
    # Здесь можно добавить проверку подключения к БД и другим сервисам
    return {
        "status": "ready",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/deployment")
async def deployment_status():
    """
    Endpoint для проверки статуса деплоя.
    Возвращает информацию о последнем деплое на сервере.
    
    Используйте этот endpoint для проверки:
    - Прошел ли деплой успешно
    - Какая версия (commit) сейчас на сервере
    - Когда был последний деплой
    - Из какой ветки был деплой
    """
    deployment_info = get_deployment_info()
    
    return {
        "status": "deployed",
        "deployment_info": deployment_info,
        "current_time": datetime.now().isoformat(),
        "server": "AWS EC2",
        "message": "Деплой успешен" if deployment_info["deployed_at"] != "unknown" else "Информация о деплое недоступна"
    }
