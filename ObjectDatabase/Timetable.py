from uuid import uuid4

from persistent import Persistent


class Timetable(Persistent):
    def __init__(self, timetable_name=None, date=None):
        self.timetable_id = uuid4()
        self.timetable_name = timetable_name
        self.date = date
