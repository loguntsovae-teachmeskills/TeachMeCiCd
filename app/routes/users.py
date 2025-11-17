"""
Роутер для работы с пользователями.
CRUD операции для демонстрации функционала API.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime

from app.models import (
    UserCreate,
    UserUpdate,
    UserResponse,
    MessageResponse
)

router = APIRouter()

# Имитация базы данных (в памяти)
# В продакшене здесь будет реальная БД (PostgreSQL, MongoDB и т.д.)
fake_users_db = {}
user_id_counter = 1


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Создание нового пользователя.
    
    - **email**: Email адрес пользователя
    - **username**: Уникальное имя пользователя
    - **password**: Пароль (будет захеширован)
    - **full_name**: Полное имя (опционально)
    """
    global user_id_counter
    
    # Проверка на существующий email
    for existing_user in fake_users_db.values():
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует"
            )
        if existing_user["username"] == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким username уже существует"
            )
    
    # Создание пользователя
    user_dict = user.model_dump()
    hashed_password = f"hashed_{user_dict.pop('password')}"  # Имитация хеширования
    
    new_user = {
        "id": user_id_counter,
        "email": user_dict["email"],
        "username": user_dict["username"],
        "full_name": user_dict.get("full_name"),
        "created_at": datetime.now(),
        "is_active": True,
        "hashed_password": hashed_password
    }
    
    fake_users_db[user_id_counter] = new_user
    user_id_counter += 1
    
    # Возвращаем данные без пароля
    return UserResponse(**new_user)


@router.get("/users", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 100):
    """
    Получение списка всех пользователей.
    
    - **skip**: Количество пропускаемых записей (для пагинации)
    - **limit**: Максимальное количество возвращаемых записей
    """
    users = list(fake_users_db.values())
    return [UserResponse(**user) for user in users[skip:skip + limit]]


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """
    Получение пользователя по ID.
    
    - **user_id**: ID пользователя
    """
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с ID {user_id} не найден"
        )
    
    return UserResponse(**fake_users_db[user_id])


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate):
    """
    Обновление данных пользователя.
    
    - **user_id**: ID пользователя
    - Поля для обновления передаются в теле запроса
    """
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с ID {user_id} не найден"
        )
    
    stored_user = fake_users_db[user_id]
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Проверка уникальности email и username при обновлении
    if "email" in update_data:
        for uid, u in fake_users_db.items():
            if uid != user_id and u["email"] == update_data["email"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email уже используется"
                )
    
    if "username" in update_data:
        for uid, u in fake_users_db.items():
            if uid != user_id and u["username"] == update_data["username"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username уже используется"
                )
    
    # Обработка пароля
    if "password" in update_data:
        stored_user["hashed_password"] = f"hashed_{update_data.pop('password')}"
    
    # Обновление полей
    for field, value in update_data.items():
        stored_user[field] = value
    
    return UserResponse(**stored_user)


@router.delete("/users/{user_id}", response_model=MessageResponse)
async def delete_user(user_id: int):
    """
    Удаление пользователя.
    
    - **user_id**: ID пользователя для удаления
    """
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с ID {user_id} не найден"
        )
    
    deleted_user = fake_users_db.pop(user_id)
    
    return MessageResponse(
        message="Пользователь успешно удален",
        detail=f"Удален пользователь: {deleted_user['username']}"
    )


@router.get("/users/search/by-username/{username}", response_model=UserResponse)
async def search_user_by_username(username: str):
    """
    Поиск пользователя по username.
    
    - **username**: Username для поиска
    """
    for user in fake_users_db.values():
        if user["username"] == username:
            return UserResponse(**user)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Пользователь с username '{username}' не найден"
    )
