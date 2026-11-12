from controllers.shared.response_handler import run
from dto.shared.request_models import SkillRequest
class SkillController:
    def __init__(self,service): self._service=service
    def create(self,data): return run(lambda:self._service.create(SkillRequest(**data)))
    def get_by_id(self,item_id): return run(lambda:self._service.get_by_id(item_id))
    def get_one(self,filters=None): return run(lambda:self._service.get_one(filters))
    def get_paginated(self,offset,limit,filters=None): return run(lambda:self._service.get_paginated(offset,limit,filters))
    def update(self,item_id,data): return run(lambda:self._service.update(item_id,SkillRequest(**data)))
    def delete(self,item_id): return run(lambda:self._service.delete(item_id))
