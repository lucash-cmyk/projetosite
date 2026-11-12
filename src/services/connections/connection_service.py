from core.errors import ValidationFailed
class ConnectionService:
    def __init__(self,repo,user_repository): self._repo=repo; self._users=user_repository
    def _validate_pair(self,a,b):
        if not self._users.get_by_id(a) or not self._users.get_by_id(b): raise ValidationFailed("Os dois usuários precisam existir.")
        if a==b: raise ValidationFailed("Você não pode se conectar consigo mesmo.")
    def create(self,user_id,connected_user_id,data): self._validate_pair(user_id,connected_user_id); return self._repo.create(user_id,connected_user_id,data)
    def connection_exists(self,user_id,connected_user_id): return self._repo.connection_exists(user_id,connected_user_id)
    def request_connection(self,user_id,connected_user_id):
        self._validate_pair(user_id,connected_user_id)
        if self._repo.connection_exists(user_id,connected_user_id): raise ValidationFailed("Já existe uma solicitação ou conexão entre esses usuários.")
        return self._repo.request_connection(user_id,connected_user_id)
    def list_all(self): return self._repo.list_all()
    def get_paginated_for_user(self,user_id,offset,limit): return self._repo.get_paginated_for_user(user_id,max(0,int(offset)),max(1,min(int(limit),100)))
    def update_connection_request(self,user_id,connected_user_id,data): return self._repo.update_connection_request(user_id,connected_user_id,data)
    def get_mutual_connections(self,user_id,connected_user_id): return self._repo.get_mutual_connections(user_id,connected_user_id)
    def get_shortest_path(self,user_id,target_user_id): return self._repo.get_shortest_path(user_id,target_user_id)
    def count_connections(self,user_id): return self._repo.count_connections(user_id)
    def update(self,user_id,connected_user_id,data): return self._repo.update(user_id,connected_user_id,data)
    def delete(self,user_id,connected_user_id): return self._repo.delete(user_id,connected_user_id)
