from persistent import Persistent

from ObjectDatabase.User import User


class Administrator(User):

    def __init__(self, surname, email, name, university, duty, timetables):
        User.__init__(self, surname=surname, email=email, name=name, university=university)
        self.duty = duty
        self.timetables = timetables
