import secrets

PREFIX = "session:"


class SessionRepository:
    """Sessões em Redis: token aleatório -> id do usuário, com expiração."""

    def __init__(self, redis_client):
        self._redis = redis_client

    def create(self, user_id, ttl_seconds):
        token = secrets.token_urlsafe(32)
        self._redis.setex(PREFIX + token, ttl_seconds, user_id)
        return token

    def get_user_id(self, token, ttl_seconds):
        key = PREFIX + token
        value = self._redis.get(key)
        if value is None:
            return None
        self._redis.expire(key, ttl_seconds)  # renova a sessão enquanto houver uso
        return value.decode("utf-8") if isinstance(value, bytes) else value

    def delete(self, token):
        self._redis.delete(PREFIX + token)
