from datetime import datetime, timezone
from core.errors import NotFound, ValidationFailed
class MentorshipService:
    def __init__(self,repo,user_repository): self._repo=repo; self._users=user_repository
    def create(self,data):
        if not self._users.get_by_id(data.user_id): raise NotFound("Usuário não encontrado.")
        return self._repo.create({**data.model_dump(),"created_at":datetime.now(timezone.utc)})
    def get_by_id(self,item_id):
        item=self._repo.get_by_id(item_id)
        if not item: raise NotFound("Perfil de mentoria não encontrado.")
        return item
    def filter_mentors(self,filters=None): return self._repo.filter_mentors(filters)
    def get_by_user_id(self,user_id): return self._repo.get_by_user_id(user_id)
    def list_all(self): return self._repo.list_all()
    def update(self,item_id,data): self.get_by_id(item_id); self._repo.update(item_id,data); return self.get_by_id(item_id)
    def delete(self,item_id): self.get_by_id(item_id); return self._repo.delete(item_id)
