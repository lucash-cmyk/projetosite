from controllers.shared.response_handler import run
class UserSkillController:
    def __init__(self,service): self._service=service
    def add_skill(self,user_id,skill_id,skill_type): return run(lambda:self._service.add_skill(user_id,skill_id,skill_type))
    def remove_skill(self,user_id,skill_id,skill_type): return run(lambda:self._service.remove_skill(user_id,skill_id,skill_type))
    def get_skills(self,filters=None): return run(lambda:self._service.get_skills(filters))
