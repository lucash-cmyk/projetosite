from pymongo.errors import DuplicateKeyError

from core.errors import ValidationFailed
from repositories.shared.mongo_utils import serialize, to_object_id


class UserRepository:
    def __init__(self, database):
        self._users = database["users"]
        self._users.create_index("email", unique=True)

    def create(self, data):
        doc = dict(data)
        try:
            self._users.insert_one(doc)
        except DuplicateKeyError as exc:
            raise ValidationFailed("E-mail já cadastrado.") from exc
        return serialize(doc)

    def get_by_id(self, user_id):
        oid = to_object_id(user_id)
        if oid is None:
            return None
        return serialize(self._users.find_one({"_id": oid}))

    def get_by_email(self, email):
        return serialize(self._users.find_one({"email": email}))

    def get_many_by_ids(self, user_ids):
        oids = [o for o in (to_object_id(i) for i in user_ids) if o is not None]
        if not oids:
            return {}
        docs = (serialize(d) for d in self._users.find({"_id": {"$in": oids}}))
        return {d["id"]: d for d in docs}

    def update_profile(self, user_id, data):
        oid = to_object_id(user_id)
        if oid is None:
            return False
        return self._users.update_one({"_id": oid}, {"$set": data}).matched_count > 0
