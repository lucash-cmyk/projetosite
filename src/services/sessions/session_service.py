from core.errors import AuthenticationFailed

SESSION_TTL_SECONDS = 8 * 60 * 60


class SessionService:
    def __init__(self, session_repository, user_service):
        self._sessions = session_repository
        self._users = user_service

    def login(self, email, password):
        user = self._users.authenticate(email, password)
        token = self._sessions.create(user["id"], SESSION_TTL_SECONDS)
        return {"token": token, "user": user}

    def resolve(self, token):
        """Usuário dono do token, ou None se a sessão não existir/expirou."""
        if not token:
            return None
        user_id = self._sessions.get_user_id(token, SESSION_TTL_SECONDS)
        if not user_id:
            return None
        try:
            return self._users.get_by_id(user_id)
        except Exception:
            return None

    def logout(self, token):
        if token:
            self._sessions.delete(token)

    def require_user(self, token):
        user = self.resolve(token)
        if user is None:
            raise AuthenticationFailed("Sessão expirada. Entre novamente.")
        return user
