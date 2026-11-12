from controllers.shared.response_handler import run
from dto.shared.request_models import OrganizationRequest
class OrganizationController:
    def __init__(self,service): self._service=service
    def create(self,data): return run(lambda:self._service.create(OrganizationRequest(**data)))
    def get_by_id(self,item_id): return run(lambda:self._service.get_by_id(item_id))
    def get_paginated(self,offset,limit,filters=None): return run(lambda:self._service.get_paginated(offset,limit,filters))
    def list_all(self): return run(self._service.list_all)
    def update(self,item_id,data): return run(lambda:self._service.update(item_id,OrganizationRequest(**data)))
    def delete(self,item_id): return run(lambda:self._service.delete(item_id))
