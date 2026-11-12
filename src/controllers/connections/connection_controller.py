from controllers.shared.response_handler import run
from dto.shared.request_models import ConnectionRequest
class ConnectionController:
    def __init__(self,service): self._service=service
    def create(self,user_id,connected_user_id,data): return run(lambda:self._service.create(user_id,connected_user_id,ConnectionRequest(**data).model_dump()))
    def connection_exists(self,user_id,connected_user_id): return run(lambda:self._service.connection_exists(user_id,connected_user_id))
    def request_connection(self,user_id,connected_user_id): return run(lambda:self._service.request_connection(user_id,connected_user_id))
    def list_all(self): return run(self._service.list_all)
    def get_paginated_for_user(self,user_id,offset,limit): return run(lambda:self._service.get_paginated_for_user(user_id,offset,limit))
    def update_connection_request(self,user_id,connected_user_id,data): return run(lambda:self._service.update_connection_request(user_id,connected_user_id,ConnectionRequest(**data).model_dump()))
    def get_mutual_connections(self,user_id,connected_user_id): return run(lambda:self._service.get_mutual_connections(user_id,connected_user_id))
    def get_shortest_path(self,user_id,target_user_id): return run(lambda:self._service.get_shortest_path(user_id,target_user_id))
    def count_connections(self,user_id): return run(lambda:self._service.count_connections(user_id))
    def update(self,user_id,connected_user_id,data): return run(lambda:self._service.update(user_id,connected_user_id,ConnectionRequest(**data).model_dump(exclude_unset=True)))
    def delete(self,user_id,connected_user_id): return run(lambda:self._service.delete(user_id,connected_user_id))
