"""
Тесты для health check endpoints.
Smoke тесты для проверки работоспособности приложения.
"""

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.smoke
def test_health_check():
    """Тест основного health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert data["version"] == "1.0.2"
    assert data["database"] == "ok"
    assert "timestamp" in data


@pytest.mark.smoke
def test_kubernetes_health():
    """Тест упрощенного health check для Kubernetes."""
    response = client.get("/healthz")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"


@pytest.mark.smoke
def test_kubernetes_ready():
    """Тест readiness check для Kubernetes."""
    response = client.get("/readyz")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ready"
    assert "timestamp" in data


@pytest.mark.smoke
def test_root_endpoint():
    """Тест корневого endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()

    assert "message" in data
    assert data["version"] == "1.0.2"
    assert data["docs"] == "/docs"


@pytest.mark.smoke
def test_deployment_endpoint():
    """Тест deployment status endpoint."""
    response = client.get("/deployment")

    assert response.status_code == 200
    data = response.json()

    # Проверяем основную структуру ответа
    assert "status" in data
    assert "deployment_info" in data
    assert "current_time" in data
    assert "server" in data
    assert "message" in data

    # Проверяем структуру deployment_info
    deployment_info = data["deployment_info"]
    assert "deployed_at" in deployment_info
    assert "commit_sha" in deployment_info
    assert "branch" in deployment_info
    assert "deployed_by" in deployment_info

    # Проверяем значения
    assert data["status"] == "deployed"
    assert data["server"] == "AWS EC2"
