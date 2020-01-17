from uuid import uuid4

from persistent import Persistent


class Welcomepack(Persistent):
    def __init__(self, shirt_size=None):
        self.welcomepack_id = uuid4()
        self.shirt_size = shirt_size
