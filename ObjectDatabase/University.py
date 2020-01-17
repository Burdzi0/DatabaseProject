from persistent import Persistent
from uuid import uuid4


class University(Persistent):

    def __init__(self, uni_name=None,  postal_code=None, town=None, address=None, country=None):
        self.university_id = uuid4()
        self.uni_name = uni_name
        self.postal_code = postal_code
        self.town = town
        self.address = address
        self.country = country
