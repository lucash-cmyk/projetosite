import json
from datetime import datetime, timezone

PREFIX="presence:"
class OnlinePresenceRepository:
    def __init__(self,redis_client): self._redis=redis_client
    def create(self,data):
        user_id=data["user_id"]; payload={**data,"last_seen":datetime.now(timezone.utc).isoformat()}; self._redis.set(PREFIX+user_id,json.dumps(payload)); return payload
    def get_by_user_id(self,user_id):
        raw=self._redis.get(PREFIX+user_id)
        if raw is None: return None
        if isinstance(raw,bytes): raw=raw.decode()
        return json.loads(raw)
    def create_last_seen(self,user_id): return self.update_last_seen(user_id)
    def update_last_seen(self,user_id):
        current=self.get_by_user_id(user_id) or {"user_id":user_id}
        current["last_seen"]=datetime.now(timezone.utc).isoformat(); self._redis.set(PREFIX+user_id,json.dumps(current)); return current
    def delete_last_seen(self,user_id): return self._redis.delete(PREFIX+user_id)>0
    def get_paginated(self,offset,limit,filters=None):
        # Redis não oferece paginação eficiente por prefixo; SCAN evita bloquear o servidor.
        keys=list(self._redis.scan_iter(match=PREFIX+"*")); values=[]
        for key in keys:
            raw=self._redis.get(key)
            if raw:
                if isinstance(raw,bytes): raw=raw.decode()
                values.append(json.loads(raw))
        values.sort(key=lambda x:x.get("last_seen", ""),reverse=True)
        return values[offset:offset+limit]
    def update(self,user_id,data):
        current=self.get_by_user_id(user_id)
        if not current: return False
        current.update(data); self._redis.set(PREFIX+user_id,json.dumps(current)); return True
    def delete(self,user_id): return self.delete_last_seen(user_id)
