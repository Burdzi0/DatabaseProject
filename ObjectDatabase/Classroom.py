from uuid import uuid4

from persistent import Persistent


class Classroom(Persistent):
    def __init__(self, classroom_number=None, postal_code=None, town=None, address=None):
        self.classroom_id = uuid4()
        self.classroom_number = classroom_number
        self.postal_code = postal_code
        self.town = town
        self.address = address
