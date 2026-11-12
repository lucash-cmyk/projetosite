from controllers.shared.response_handler import run
from dto.shared.request_models import MentorshipRequest
class MentorshipController:
    def __init__(self,service): self._service=service
    def create(self,data): return run(lambda:self._service.create(MentorshipRequest(**data)))
    def get_by_id(self,item_id): return run(lambda:self._service.get_by_id(item_id))
    def filter_mentors(self,filters=None): return run(lambda:self._service.filter_mentors(filters))
    def get_by_user_id(self,user_id): return run(lambda:self._service.get_by_user_id(user_id))
    def list_all(self): return run(self._service.list_all)
    def update(self,item_id,data): return run(lambda:self._service.update(item_id,data))
    def delete(self,item_id): return run(lambda:self._service.delete(item_id))
