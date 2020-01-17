from ObjectDatabase.User import User
from persistent import Persistent


class Reviewer(User):

    def __init__(self, surname, email, name, university, academic_title, domains, grades):
        User.__init__(self, surname=surname, email=email, name=name, university=university)
        self.academic_title = academic_title
        self.domains = domains
        self.grades = grades

