from uuid import uuid4

from persistent import Persistent


class Event(Persistent):

    def __init__(self, name=None, organizing_body=None, address=None, postal_code=None, town=None, timetables=None):
        self.event_id = uuid4()
        self.name = name
        self.organizing_body = organizing_body
        self.address = address
        self.postal_code = postal_code
        self.town = town
        self.timetables = timetables
