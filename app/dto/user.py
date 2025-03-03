# app/dto/user.py

from typing import List

from app.models.user import User


class UserDTO:
    def __init__(self, user: User):
        self.username = user.username
        self.role = user.role
        self.url = user.url

    def to_dict(self):
        return {
            "username": self.username,
            "role": self.role.name,
            "url": self.url,
        }

    @staticmethod
    def from_model(user: User) -> dict:
        return UserDTO(user).to_dict() if user else None

    @staticmethod
    def from_model_list(users: List[User]) -> list:
        return [UserDTO(user).to_dict() for user in users]
