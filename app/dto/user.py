# app/dto/user.py


from typing import List

from app.config import Config
from app.models.user import User


class UserDTO:
    def __init__(self, user: User):
        self.user_id = str(user.user_id)
        self.username = user.username
        self.role = user.role

    def to_dict(self):
        return {
            "url": f"{Config.APP_URL}{Config.API_URI}/users/{self.user_id}",
            "id": self.user_id,
            "username": self.username,
            "role": self.role.name,
        }

    @staticmethod
    def from_model(user: User) -> dict:
        return UserDTO(user).to_dict() if user else {}

    @staticmethod
    def from_model_list(users: List[User]) -> list[dict]:
        return [UserDTO(user).to_dict() for user in users]
