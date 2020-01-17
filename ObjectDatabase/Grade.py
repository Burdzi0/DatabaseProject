from uuid import uuid4

from persistent import Persistent


class Grade(Persistent):

    def __init__(self, paper_id=None, user_id=None, grade=None, reason=None):
        self.grade_id = uuid4()
        self.paper_id = paper_id
        self.user_id = user_id
        self.grade = grade
        self.reason = reason
