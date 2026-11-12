from controllers.shared.response_handler import run
from dto.shared.request_models import NotificationRequest
class NotificationController:
    def __init__(self,service): self._service=service
    def create(self,data): return run(lambda:self._service.create(NotificationRequest(**data)))
    def get_by_id(self,item_id): return run(lambda:self._service.get_by_id(item_id))
    def get_paginated(self,offset,limit,filters=None): return run(lambda:self._service.get_paginated(offset,limit,filters))
    def count_unread_by_user_id(self,user_id): return run(lambda:self._service.count_unread_by_user_id(user_id))
    def mark_all_as_read(self,user_id): return run(lambda:self._service.mark_all_as_read(user_id))
    def update(self,item_id,data): return run(lambda:self._service.update(item_id,data))
    def delete(self,item_id): return run(lambda:self._service.delete(item_id))
