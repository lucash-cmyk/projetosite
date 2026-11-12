from datetime import datetime, timezone
from core.errors import NotFound, ValidationFailed
class SkillService:
    def __init__(self,repo): self._repo=repo
    def create(self,data):
        try: return self._repo.create({**data.model_dump(),"created_at":datetime.now(timezone.utc)})
        except Exception as exc:
            if "duplicate" in str(exc).lower(): raise ValidationFailed("Esta habilidade já está cadastrada.") from exc
            raise
    def get_by_id(self,item_id):
        item=self._repo.get_by_id(item_id)
        if not item: raise NotFound("Habilidade não encontrada.")
        return item
    def get_one(self,filters=None): return self._repo.get_one(filters)
    def get_paginated(self,offset,limit,filters=None): return self._repo.get_paginated(max(0,int(offset)),max(1,min(int(limit),100)),filters)
    def update(self,item_id,data): self.get_by_id(item_id); self._repo.update(item_id,data.model_dump(exclude_unset=True)); return self.get_by_id(item_id)
    def delete(self,item_id): self.get_by_id(item_id); return self._repo.delete(item_id)
