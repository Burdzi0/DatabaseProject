from uuid import uuid4

from persistent import Persistent


class Domain(Persistent):

    def __init__(self, domain_name):
        self.domain_id = uuid4()
        self.domain_name = domain_name
