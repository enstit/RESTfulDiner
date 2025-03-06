# app/dto/user.py

from typing import List

from app.config import Config
from app.models.user import User


class UserDTO:
    def __init__(self, user: User):
        self.id = str(user.id)
        self.username = user.username
        self.role = user.role

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role.name,
        }

    @staticmethod
    def from_model(user: User) -> dict:
        return UserDTO(user).to_dict() if user else None

    @staticmethod
    def from_model_list(users: List[User]) -> list:
        return [UserDTO(user).to_dict() for user in users]
