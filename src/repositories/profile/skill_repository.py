from pymongo import ASCENDING
from repositories.shared.mongo_utils import serialize, to_object_id

class SkillRepository:
    def __init__(self, database):
        self._items=database["skills"]; self._items.create_index("name",unique=True)
    def create(self,data):
        doc=dict(data); self._items.insert_one(doc); return serialize(doc)
    def get_by_id(self,item_id):
        oid=to_object_id(item_id); return serialize(self._items.find_one({"_id":oid})) if oid else None
    def get_one(self,filters=None): return serialize(self._items.find_one(filters or {}))
    def get_paginated(self,offset,limit,filters=None):
        q={k:v for k,v in (filters or {}).items() if k in {"category"} and v}
        return [serialize(x) for x in self._items.find(q).sort("name",ASCENDING).skip(offset).limit(limit)]
    def update(self,item_id,data):
        oid=to_object_id(item_id); return bool(oid and self._items.update_one({"_id":oid},{"$set":data}).matched_count)
    def delete(self,item_id):
        oid=to_object_id(item_id); return bool(oid and self._items.delete_one({"_id":oid}).deleted_count)
