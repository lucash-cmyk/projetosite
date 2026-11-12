from controllers.shared.response_handler import run
from dto.profile.request.user_requests import RegisterRequest, UpdateProfileRequest


class UserController:
    def __init__(self, user_service):
        self._service = user_service

    def register(self, data: dict):
        return run(lambda: self._service.register(RegisterRequest(**data)))

    def get_by_id(self, user_id):
        return run(lambda: self._service.get_by_id(user_id))

    def update_profile(self, user_id, data: dict):
        return run(lambda: self._service.update_profile(user_id, UpdateProfileRequest(**data)))

    def get_by_email(self, email: str):
        return run(lambda: self._service.get_by_email(email))
