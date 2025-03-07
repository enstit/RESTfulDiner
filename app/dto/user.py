# app/dto/user.py

from typing import List

from app.config import Config
from app.models.user import User


class UserDTO:

    CONTEXT = {
        "@context": {
            "schema": "https://schema.org/",
            "self": "@id",
            "type": "@type",
            "username": "schema:name",
            "role": "schema:hasOccupation",
            "license": {"@id": "schema:license", "@type": "@id"},
        },
        "license": "https://creativecommons.org/licenses/by/4.0/",
    }

    def __init__(self, user: User):
        self.id = str(user.id)
        self.username = user.username
        self.role = user.role

    def to_dict(self):
        return {
            "self": f"{Config.APP_URL}{Config.API_URI}/users/{self.id}",
            "type": "schema:Person",
            "username": self.username,
            "role": self.role.name,
        }

    @staticmethod
    def from_model(user: User) -> dict:
        return (
            {
                **UserDTO.CONTEXT,
                "data": UserDTO(user).to_dict(),
            }
            if user
            else None
        )

    @staticmethod
    def from_model_list(users: List[User]) -> dict:
        return {
            **UserDTO.CONTEXT,
            "data": [UserDTO(user).to_dict() for user in users],
        }
