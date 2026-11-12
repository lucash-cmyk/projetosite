from controllers.shared.response_handler import run


class MediaController:
    def __init__(self, media_service):
        self._service = media_service

    def get(self, file_id):
        return run(lambda: self._service.get(file_id))
