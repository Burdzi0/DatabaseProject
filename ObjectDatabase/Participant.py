from persistent import Persistent

from ObjectDatabase.User import User


class Participant(User):

    def __init__(self, surname, email, name, university, welcomepack, ticket, timetables):
        User.__init__(self, surname=surname, email=email, name=name, university=university)
        self.welcomepack = welcomepack
        self.ticket = ticket
        self.timetables = timetables
