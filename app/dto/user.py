from app.models.user import User


class UserDTO:
    def __init__(self, user: User):
        self.username = user.username

    def to_dict(self):
        return {"username": self.username}

    @staticmethod
    def from_model(user):
        return UserDTO(user).to_dict() if user else None

    @staticmethod
    def from_model_list(users):
        return [UserDTO(user).to_dict() for user in users]
