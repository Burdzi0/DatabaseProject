from persistent import Persistent
from uuid import uuid4
import datetime


class User(Persistent):

    def __init__(self, surname, email, name, university):
        self.user_id = uuid4()
        self.university = university
        self.name = name
        self.email = email
        self.surname = surname
        self.registration_date = datetime.date.today()
