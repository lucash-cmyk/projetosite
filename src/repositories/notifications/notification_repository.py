from datetime import datetime, timezone
from pymongo import DESCENDING
from repositories.shared.mongo_utils import serialize, to_object_id

class NotificationRepository:
    def __init__(self,database):
        self._items=database["notifications"]; self._items.create_index([("user_id",1),("created_at",DESCENDING)])
    def create(self,data):
        doc={**data,"read":False,"created_at":datetime.now(timezone.utc)}; self._items.insert_one(doc); return serialize(doc)
    def get_by_id(self,item_id):
        oid=to_object_id(item_id); return serialize(self._items.find_one({"_id":oid})) if oid else None
    def get_paginated(self,offset,limit,filters=None):
        q={k:v for k,v in (filters or {}).items() if k in {"user_id","read","kind"} and v is not None}
        return [serialize(x) for x in self._items.find(q).sort("created_at",DESCENDING).skip(offset).limit(limit)]
    def count_unread_by_user_id(self,user_id): return self._items.count_documents({"user_id":user_id,"read":False})
    def mark_all_as_read(self,user_id): return self._items.update_many({"user_id":user_id,"read":False},{"$set":{"read":True}}).modified_count
    def update(self,item_id,data):
        oid=to_object_id(item_id); return bool(oid and self._items.update_one({"_id":oid},{"$set":data}).matched_count)
    def delete(self,item_id):
        oid=to_object_id(item_id); return bool(oid and self._items.delete_one({"_id":oid}).deleted_count)
