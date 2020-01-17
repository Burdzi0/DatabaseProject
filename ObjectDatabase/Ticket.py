from uuid import uuid4

from persistent import Persistent


class Ticket(Persistent):
    def __init__(self, cost, purchase_date):
        self.ticket_id = uuid4()
        self.cost = cost
        self.purchase_date = purchase_date
