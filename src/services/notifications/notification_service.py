from core.errors import NotFound
class NotificationService:
    def __init__(self,repo,redis_client=None): self._repo=repo; self._redis=redis_client
    def create(self,data):
        item=self._repo.create(data.model_dump() if hasattr(data,"model_dump") else dict(data))
        if self._redis: self._redis.incr(f"notifications:unread:{item['user_id']}")
        return item
    def get_by_id(self,item_id):
        item=self._repo.get_by_id(item_id)
        if not item: raise NotFound("Notificação não encontrada.")
        return item
    def get_paginated(self,offset,limit,filters=None): return self._repo.get_paginated(max(0,int(offset)),max(1,min(int(limit),100)),filters)
    def count_unread_by_user_id(self,user_id):
        key=f"notifications:unread:{user_id}"
        if self._redis:
            cached=self._redis.get(key)
            if cached is not None:
                return int(cached.decode("utf-8") if isinstance(cached,bytes) else cached)
        total=self._repo.count_unread_by_user_id(user_id)
        if self._redis: self._redis.set(key,total)
        return total
    def mark_all_as_read(self,user_id):
        changed=self._repo.mark_all_as_read(user_id)
        if self._redis: self._redis.set(f"notifications:unread:{user_id}",0)
        return changed
    def update(self,item_id,data):
        current=self.get_by_id(item_id)
        updated=self._repo.update(item_id,data)
        if self._redis and "read" in data and bool(data["read"]) != bool(current.get("read")):
            key=f"notifications:unread:{current['user_id']}"
            self.count_unread_by_user_id(current["user_id"])
            if data["read"]: self._redis.decr(key)
            else: self._redis.incr(key)
        return updated
    def delete(self,item_id): self.get_by_id(item_id); return self._repo.delete(item_id)
