"""
Интеграционные тесты для API пользователей.
Проверка CRUD операций через HTTP endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_users_db():
    """Очистка базы данных пользователей перед каждым тестом."""
    from app.routes.users import fake_users_db, user_id_counter
    fake_users_db.clear()
    # Сброс счетчика (не идеально, но работает для тестов)
    yield
    fake_users_db.clear()


@pytest.mark.integration
class TestUserCRUD:
    """Тесты CRUD операций для пользователей."""
    
    def test_create_user(self):
        """Тест создания нового пользователя."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
            "full_name": "Test User"
        }
        
        response = client.post("/api/v1/users", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert data["full_name"] == user_data["full_name"]
        assert "id" in data
        assert "created_at" in data
        assert data["is_active"] is True
        assert "password" not in data  # Пароль не должен возвращаться
    
    def test_create_user_duplicate_email(self):
        """Тест создания пользователя с существующим email."""
        user_data = {
            "email": "duplicate@example.com",
            "username": "user1",
            "password": "password123"
        }
        
        # Создаем первого пользователя
        response1 = client.post("/api/v1/users", json=user_data)
        assert response1.status_code == 201
        
        # Пытаемся создать второго с тем же email
        user_data2 = {
            "email": "duplicate@example.com",
            "username": "user2",
            "password": "password123"
        }
        response2 = client.post("/api/v1/users", json=user_data2)
        
        assert response2.status_code == 400
        assert "email" in response2.json()["detail"].lower()
    
    def test_create_user_duplicate_username(self):
        """Тест создания пользователя с существующим username."""
        user_data = {
            "email": "user1@example.com",
            "username": "duplicate",
            "password": "password123"
        }
        
        response1 = client.post("/api/v1/users", json=user_data)
        assert response1.status_code == 201
        
        user_data2 = {
            "email": "user2@example.com",
            "username": "duplicate",
            "password": "password123"
        }
        response2 = client.post("/api/v1/users", json=user_data2)
        
        assert response2.status_code == 400
        assert "username" in response2.json()["detail"].lower()
    
    def test_get_users_empty(self):
        """Тест получения списка пользователей (пустой список)."""
        response = client.get("/api/v1/users")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_users_list(self):
        """Тест получения списка пользователей."""
        # Создаем несколько пользователей
        for i in range(3):
            user_data = {
                "email": f"user{i}@example.com",
                "username": f"user{i}",
                "password": "password123"
            }
            client.post("/api/v1/users", json=user_data)
        
        response = client.get("/api/v1/users")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
    
    def test_get_user_by_id(self):
        """Тест получения пользователя по ID."""
        # Создаем пользователя
        user_data = {
            "email": "getuser@example.com",
            "username": "getuser",
            "password": "password123"
        }
        create_response = client.post("/api/v1/users", json=user_data)
        user_id = create_response.json()["id"]
        
        # Получаем пользователя по ID
        response = client.get(f"/api/v1/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == user_data["email"]
    
    def test_get_user_not_found(self):
        """Тест получения несуществующего пользователя."""
        response = client.get("/api/v1/users/999")
        
        assert response.status_code == 404
        assert "не найден" in response.json()["detail"].lower()
    
    def test_update_user(self):
        """Тест обновления данных пользователя."""
        # Создаем пользователя
        user_data = {
            "email": "update@example.com",
            "username": "updateuser",
            "password": "password123"
        }
        create_response = client.post("/api/v1/users", json=user_data)
        user_id = create_response.json()["id"]
        
        # Обновляем данные
        update_data = {
            "full_name": "Updated Name",
            "email": "newemail@example.com"
        }
        response = client.put(f"/api/v1/users/{user_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == update_data["full_name"]
        assert data["email"] == update_data["email"]
        assert data["username"] == user_data["username"]  # Не изменился
    
    def test_update_user_not_found(self):
        """Тест обновления несуществующего пользователя."""
        update_data = {"full_name": "New Name"}
        response = client.put("/api/v1/users/999", json=update_data)
        
        assert response.status_code == 404
    
    def test_delete_user(self):
        """Тест удаления пользователя."""
        # Создаем пользователя
        user_data = {
            "email": "delete@example.com",
            "username": "deleteuser",
            "password": "password123"
        }
        create_response = client.post("/api/v1/users", json=user_data)
        user_id = create_response.json()["id"]
        
        # Удаляем пользователя
        response = client.delete(f"/api/v1/users/{user_id}")
        
        assert response.status_code == 200
        assert "успешно удален" in response.json()["message"].lower()
        
        # Проверяем, что пользователь действительно удален
        get_response = client.get(f"/api/v1/users/{user_id}")
        assert get_response.status_code == 404
    
    def test_delete_user_not_found(self):
        """Тест удаления несуществующего пользователя."""
        response = client.delete("/api/v1/users/999")
        
        assert response.status_code == 404
    
    def test_search_user_by_username(self):
        """Тест поиска пользователя по username."""
        # Создаем пользователя
        user_data = {
            "email": "search@example.com",
            "username": "searchuser",
            "password": "password123"
        }
        client.post("/api/v1/users", json=user_data)
        
        # Ищем пользователя
        response = client.get("/api/v1/users/search/by-username/searchuser")
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "searchuser"
    
    def test_search_user_by_username_not_found(self):
        """Тест поиска несуществующего пользователя по username."""
        response = client.get("/api/v1/users/search/by-username/nonexistent")
        
        assert response.status_code == 404


@pytest.mark.integration
class TestUserValidation:
    """Тесты валидации данных пользователей."""
    
    def test_create_user_invalid_email(self):
        """Тест создания пользователя с невалидным email."""
        user_data = {
            "email": "invalid-email",
            "username": "testuser",
            "password": "password123"
        }
        
        response = client.post("/api/v1/users", json=user_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_create_user_short_username(self):
        """Тест создания пользователя с коротким username."""
        user_data = {
            "email": "test@example.com",
            "username": "ab",  # Меньше минимума (3)
            "password": "password123"
        }
        
        response = client.post("/api/v1/users", json=user_data)
        
        assert response.status_code == 422
    
    def test_create_user_short_password(self):
        """Тест создания пользователя с коротким паролем."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "12345"  # Меньше минимума (6)
        }
        
        response = client.post("/api/v1/users", json=user_data)
        
        assert response.status_code == 422
    
    def test_create_user_missing_required_fields(self):
        """Тест создания пользователя без обязательных полей."""
        user_data = {
            "email": "test@example.com"
            # Отсутствуют username и password
        }
        
        response = client.post("/api/v1/users", json=user_data)
        
        assert response.status_code == 422
