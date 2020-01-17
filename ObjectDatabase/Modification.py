from uuid import uuid4

from persistent import Persistent


class Modification(Persistent):
    def __init__(self, lecture_last=None, lecture_new=None):
        self.modification_id = uuid4()
        self.lecture_last = lecture_last
        self.lecture_new = lecture_new
