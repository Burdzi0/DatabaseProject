from uuid import uuid4

from persistent import Persistent


class Paper(Persistent):
    def __init__(self, user_id=None, domain_id=None, topic=None, grades=None):
        self.paper_id = uuid4()
        self.user_id = user_id
        self.domain_id = domain_id
        self.topic = topic
        self.grades = grades
