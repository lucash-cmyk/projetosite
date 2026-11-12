from repositories.shared.mongo_utils import serialize, to_object_id

class UserSkillRepository:
    def __init__(self,database):
        self._items=database["user_skills"]; self._items.create_index([("user_id",1),("skill_id",1),("skill_type",1)],unique=True)
    def add_skill(self,user_id,skill_id,skill_type):
        doc={"user_id":user_id,"skill_id":skill_id,"skill_type":skill_type}; self._items.update_one(doc,{"$setOnInsert":doc},upsert=True); return doc
    def remove_skill(self,user_id,skill_id,skill_type): return self._items.delete_one({"user_id":user_id,"skill_id":skill_id,"skill_type":skill_type}).deleted_count>0
    def get_skills(self,filters=None): return [serialize(x) for x in self._items.find(filters or {})]
