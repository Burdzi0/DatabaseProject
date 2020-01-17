from uuid import uuid4

from persistent import Persistent


class Prelection(Persistent):
    def __init__(self, classroom_id=None, lecture_id=None, timetable_id=None, start_time=None, duration=None):
        self.prelection_id = uuid4()
        self.classroom_id = classroom_id
        self.lecture_id = lecture_id
        self.timetable_id = timetable_id
        self.start_time = start_time
        self.duration = duration
