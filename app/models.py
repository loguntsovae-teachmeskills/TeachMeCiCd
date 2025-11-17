"""
Модели данных для приложения.
Используем Pydantic для валидации данных.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Базовая модель пользователя."""
    email: EmailStr = Field(..., description="Email пользователя")
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    full_name: Optional[str] = Field(None, max_length=100, description="Полное имя")


class UserCreate(UserBase):
    """Модель для создания пользователя."""
    password: str = Field(..., min_length=6, description="Пароль (минимум 6 символов)")


class UserUpdate(BaseModel):
    """Модель для обновления пользователя."""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=6)


class UserResponse(UserBase):
    """Модель для ответа с данными пользователя."""
    id: int = Field(..., description="ID пользователя")
    created_at: datetime = Field(..., description="Дата создания")
    is_active: bool = Field(default=True, description="Активен ли пользователь")

    class Config:
        from_attributes = True  # Для совместимости с ORM


class UserInDB(UserResponse):
    """Модель пользователя в базе данных."""
    hashed_password: str


class MessageResponse(BaseModel):
    """Стандартная модель ответа с сообщением."""
    message: str
    detail: Optional[str] = None


class HealthResponse(BaseModel):
    """Модель для health check endpoint."""
    status: str = Field(..., description="Статус приложения")
    timestamp: datetime = Field(..., description="Время проверки")
    version: str = Field(..., description="Версия приложения")
    database: str = Field(default="ok", description="Статус подключения к БД")


class ErrorResponse(BaseModel):
    """Модель для ошибок."""
    detail: str
    error_code: Optional[str] = None
