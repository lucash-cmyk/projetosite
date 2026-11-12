from controllers.shared.response_handler import run
from dto.sessions.request.session_requests import LoginRequest


class SessionController:
    def __init__(self, session_service):
        self._service = session_service

    def login(self, data: dict):
        def action():
            request = LoginRequest(**data)
            return self._service.login(request.email, request.password)

        return run(action)

    def resolve(self, token):
        return run(lambda: self._service.resolve(token))

    def logout(self, token):
        return run(lambda: self._service.logout(token))
