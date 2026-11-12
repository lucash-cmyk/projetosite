from pymongo import DESCENDING
from repositories.shared.mongo_utils import serialize, to_object_id

class MentorshipRepository:
    def __init__(self,database):
        self._items=database["mentorships"]; self._items.create_index("user_id"); self._items.create_index("skills")
    def create(self,data):
        doc=dict(data); self._items.insert_one(doc); return serialize(doc)
    def get_by_id(self,item_id):
        oid=to_object_id(item_id); return serialize(self._items.find_one({"_id":oid})) if oid else None
    def filter_mentors(self,filters=None):
        q={k:v for k,v in (filters or {}).items() if k in {"user_id"} and v}
        if (filters or {}).get("skill"): q["skills"]=(filters or {})["skill"]
        return [serialize(x) for x in self._items.find(q).sort("created_at",DESCENDING)]
    def get_by_user_id(self,user_id): return [serialize(x) for x in self._items.find({"user_id":user_id})]
    def list_all(self): return [serialize(x) for x in self._items.find().sort("created_at",DESCENDING)]
    def update(self,item_id,data):
        oid=to_object_id(item_id); return bool(oid and self._items.update_one({"_id":oid},{"$set":data}).matched_count)
    def delete(self,item_id):
        oid=to_object_id(item_id); return bool(oid and self._items.delete_one({"_id":oid}).deleted_count)
