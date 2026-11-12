from core.errors import NotFound
class OnlinePresenceService:
    def __init__(self,repo): self._repo=repo
    def create(self,data): return self._repo.create(data)
    def get_by_user_id(self,user_id): return self._repo.get_by_user_id(user_id)
    def create_last_seen(self,user_id): return self._repo.create_last_seen(user_id)
    def update_last_seen(self,user_id): return self._repo.update_last_seen(user_id)
    def delete_last_seen(self,user_id): return self._repo.delete_last_seen(user_id)
    def get_paginated(self,offset,limit,filters=None): return self._repo.get_paginated(max(0,int(offset)),max(1,min(int(limit),100)),filters)
    def update(self,user_id,data):
        if not self._repo.get_by_user_id(user_id): raise NotFound("Presença não encontrada.")
        return self._repo.update(user_id,data)
    def delete(self,user_id): return self._repo.delete(user_id)
