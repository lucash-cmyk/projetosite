from datetime import datetime, timezone

from core.errors import AuthenticationFailed, NotFound
from core.security import PasswordHasher


def public_user(user: dict) -> dict:
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "headline": user.get("headline", ""),
        "bio": user.get("bio", ""),
        "location": user.get("location", ""),
    }


class UserService:
    def __init__(self, user_repository, hasher=None):
        self._users = user_repository
        self._hasher = hasher or PasswordHasher()

    def register(self, data):
        user = self._users.create(
            {
                "name": data.name,
                "email": data.email,
                "password_hash": self._hasher.hash(data.password),
                "headline": data.headline,
                "created_at": datetime.now(timezone.utc),
            }
        )
        return public_user(user)

    def authenticate(self, email, password):
        user = self._users.get_by_email(email)
        if not user or not self._hasher.verify(password, user["password_hash"]):
            raise AuthenticationFailed("E-mail ou senha inválidos.")
        return public_user(user)

    def get_by_id(self, user_id):
        user = self._users.get_by_id(user_id)
        if not user:
            raise NotFound("Usuário não encontrado.")
        return public_user(user)

    def update_profile(self, user_id, data):
        if not self._users.get_by_id(user_id):
            raise NotFound("Usuário não encontrado.")
        self._users.update_profile(user_id, data.model_dump())
        return self.get_by_id(user_id)

    def get_by_email(self, email):
        user = self._users.get_by_email(email)
        return public_user(user) if user else None
