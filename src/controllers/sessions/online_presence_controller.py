from controllers.shared.response_handler import run
class OnlinePresenceController:
    def __init__(self,service): self._service=service
    def create(self,data): return run(lambda:self._service.create(data))
    def get_by_user_id(self,user_id): return run(lambda:self._service.get_by_user_id(user_id))
    def create_last_seen(self,user_id): return run(lambda:self._service.create_last_seen(user_id))
    def update_last_seen(self,user_id): return run(lambda:self._service.update_last_seen(user_id))
    def delete_last_seen(self,user_id): return run(lambda:self._service.delete_last_seen(user_id))
    def get_paginated(self,offset,limit,filters=None): return run(lambda:self._service.get_paginated(offset,limit,filters))
    def update(self,user_id,data): return run(lambda:self._service.update(user_id,data))
    def delete(self,user_id): return run(lambda:self._service.delete(user_id))
