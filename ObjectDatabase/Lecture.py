from uuid import uuid4

from persistent import Persistent


class Lecture(Persistent):

    def __init__(self, paper_id=None, user_id=None):
        self.lecture_id = uuid4()
        self.paper_id = paper_id
        self.user_id = user_id
