import os
import datetime

from ZODB import FileStorage, DB
from faker import Faker
import transaction

from prettytable import PrettyTable
from ObjectDatabase.Administrator import Administrator
from ObjectDatabase.Classroom import Classroom
from ObjectDatabase.Domain import Domain
from ObjectDatabase.Event import Event
from ObjectDatabase.Grade import Grade
from ObjectDatabase.Lecture import Lecture
from ObjectDatabase.Modification import Modification
from ObjectDatabase.Paper import Paper
from ObjectDatabase.Participant import Participant
from ObjectDatabase.Prelection import Prelection
from ObjectDatabase.Reviewer import Reviewer
from ObjectDatabase.Ticket import Ticket
from ObjectDatabase.Timetable import Timetable
from ObjectDatabase.University import University
from ObjectDatabase.User import User
from ObjectDatabase.Welcomepack import Welcomepack

print('Importing finished, creating faker')

fake = Faker()
table = PrettyTable()
table.field_names = ["Lp", "User ID", "Name", "Lastname", "Email", "Registration date", "Uni name", "Uni town",
                     "Uni address",
                     "Uni country"]


if not os.path.exists("data"):
    print("Data directory does not exist, creating")
    os.makedirs("data")

print('Connecting to the file database')
storage = FileStorage.FileStorage('data/mydata.fs')
db = DB(storage)
connection = db.open()
root = connection.root()
print('Connected')

print('Creating collections')
if 'admin' not in root:
    root['admin'] = {}
if 'classroom' not in root:
    root['classroom'] = {}
if 'domain' not in root:
    root['domain'] = {}
if 'event' not in root:
    root['event'] = {}
if 'grade' not in root:
    root['grade'] = {}
if 'lecture' not in root:
    root['lecture'] = {}
if 'modification' not in root:
    root['modification'] = {}
if 'paper' not in root:
    root['paper'] = {}
if 'participant' not in root:
    root['participant'] = {}
if 'prelection' not in root:
    root['prelection'] = {}
if 'reviewer' not in root:
    root['reviewer'] = {}
if 'ticket' not in root:
    root['ticket'] = {}
if 'timetable' not in root:
    root['timetable'] = {}
if 'unis' not in root:
    root['unis'] = {}
if 'users' not in root:
    root['users'] = {}
if 'welcomepack' not in root:
    root['welcomepack'] = {}

admins = root['admin']
classrooms = root['classroom']
domains = root['domain']
events = root['event']
grades = root['grade']
lectures = root['lecture']
modifications = root['modification']
papers = root['paper']
participants = root['participant']
prelections = root['prelection']
reviewers = root['reviewer']
tickets = root['ticket']
timetables = root['timetable']
unis = root['unis']
users = root['users']
welcomepacks = root['welcomepack']

print('Creating entities (in a single transaction)')

transaction.begin()
for i in range(10):
    uni = University(fake.company(), fake.postalcode(), fake.city(), fake.address(), fake.country())
    user = User(fake.last_name(), fake.email(), fake.name(), uni)
    classroom = Classroom(fake.random_digit(), fake.postalcode(), fake.city(), fake.address())
    domain = Domain(fake.job())
    timetable = Timetable(fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None), datetime.date.today())
    admin = Administrator(user.surname, user.email, user.name, user.university, fake.job(), timetable)
    event = Event(fake.catch_phrase(), user, fake.address(), fake.postalcode(), fake.city(), timetable)
    paper = Paper(user, domain, fake.word(ext_word_list=None), {})
    grade = Grade(paper, user, fake.random_digit(), fake.word(ext_word_list=None))
    lecture = Lecture(paper, user)
    modification = Modification(lecture, lecture)
    welcomepack = Welcomepack(fake.random_letter())
    ticket = Ticket(fake.random_digit(), datetime.date.today())
    prelection = Prelection(classroom, lecture, timetable,  datetime.date.today(),  fake.random_digit())
    participant = Participant(user.surname, user.email, user.name, user.university, welcomepack, ticket, timetable)
    reviewer = Reviewer(user.surname, user.email, user.name, user.university, fake.job(), {domain}, {grade})

    users[user.user_id] = user
    unis[uni.university_id] = uni
    classrooms[classroom.classroom_id] = classroom
    domains[domain.domain_id] = domain
    timetables[timetable.timetable_id] = timetable
    events[event.event_id] = event
    papers[paper.paper_id] = paper
    grades[grade.grade_id] = grade
    lectures[lecture.lecture_id] = lecture
    modifications[modification.modification_id] = modification
    welcomepacks[welcomepack.welcomepack_id] = welcomepack
    tickets[ticket.ticket_id] = ticket
    participants[participant.user_id] = participant
    reviewers[reviewer.user_id] = reviewer
    admins[admin.user_id] = admin
    prelections[prelection.prelection_id] = prelection


root['admin'] = admins
root['classroom'] = classrooms
root['domain'] = domains
root['event'] = events
root['grade'] = grades
root['lecture'] = lectures
root['modification'] = modifications
root['paper'] = papers
root['participant'] = participants
root['prelection'] = prelections
root['reviewer'] = reviewers
root['ticket'] = tickets
root['timetable'] = timetables
root['unis'] = unis
root['users'] = users
root['welcomepack'] = welcomepacks
transaction.commit()

print('Saved')

i = 1
for us in users.values():
    un = us.university
    table.add_row(
        [i, us.user_id, us.name, us.surname, us.email, us.registration_date, un.uni_name, un.town, un.address,
         un.country])
    i += 1

print(table)

print('Closing connection')
connection.close()
print('Closed')
