from datetime import date
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Time, Float
from faker import Faker
import random
from random import randrange, randint, shuffle, seed
from faker.providers.job import Provider

meta = MetaData()

engine = create_engine('postgres://docker:docker@localhost/docker', echo=True)
meta.create_all(engine)

university = Table(
    'university', meta,
    Column('university_id', Integer, primary_key=True),
    Column('uni_name', String),
    Column('postal_code', String),
    Column('town', String),
    Column('address', String),
    Column('country', String)
)

user = Table(
    'user', meta,
    Column('user_id', Integer, primary_key=True),
    Column('university_id', Integer),
    Column('name', String),
    Column('email', String),
    Column('surname', String),
    Column('registration_date', Date)
)

event = Table(
    'event', meta,
    Column('event_id', Integer, primary_key=True),
    Column('event_name', String),
    Column('organizing_body', String),
    Column('address', String),
    Column('postal_code', String),
    Column('town', String)
)

timetable = Table(
    'timetable', meta,
    Column('timetable_id', Integer, primary_key=True),
    Column('event_id', Integer),
    Column('timetable_name', String),
    Column('date', Date)
)

classroom = Table(
    'classroom', meta,
    Column('classroom_id', Integer, primary_key=True),
    Column('classroom_number', Integer),
    Column('postal_code', String),
    Column('town', String),
    Column('address', String)
)

lecture = Table(
    'lecture', meta,
    Column('lecture_id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('classroom_id', Integer),
    Column('timetable_id', Integer),
    Column('paper_id', Integer),
    Column('start_time', Time),
    Column('duration', Integer)
)

paper = Table(
    'paper', meta,
    Column('paper_id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('domain_id', Integer),
    Column('topic', String),
    Column('abstrakt', String)
)

domain = Table(
    'domain', meta,
    Column('domain_id', Integer, primary_key=True),
    Column('domain_name', String)
)

participant = Table(
    'participant', meta,
    Column('welcomepack_id', Integer),
    Column('ticket_id', Integer),
    Column('user_id', Integer, primary_key=True)
)

welcomepack = Table(
    'welcomepack', meta,
    Column('welcomepack_id', Integer, primary_key=True),
    Column('shirt_size', String)
)

ticket = Table(
    'ticket', meta,
    Column('ticket_id', Integer, primary_key=True),
    Column('cost', Float),
    Column('purchase_date', Date)
)

grade = Table(
    'grade', meta,
    Column('paper_id', Integer, primary_key=True),
    Column('user_id', Integer, primary_key=True),
    Column('grade', Float),
    Column('reason', String)
)

reviewer = Table(
    'reviewer', meta,
    Column('user_id', Integer, primary_key=True),
    Column('academic_title', String)
)

administrator = Table(
    'administrator', meta,
    Column('user_id', Integer, primary_key=True),
    Column('duty', String)
)

supervision = Table(
    'supervision', meta,
    Column('user_id', Integer, primary_key=True),
    Column('timetable_id', Integer, primary_key=True)
)

domain_reviewer = Table(
    'domain_reviewer', meta,
    Column('user_id', Integer, primary_key=True),
    Column('domain_id', Integer, primary_key=True)
)

participation = Table(
    'participation', meta,
    Column('user_id', Integer, primary_key=True),
    Column('lecture_id', Integer, primary_key=True)
)

conn = engine.connect()
fake = Faker()


def generate_domains():
    domains = list(set(Provider.job))
    seed(2020)
    shuffle(domains)

    for dom in range(20):
        insert_domain = domain.insert().values(domain_name=domains[dom])
        conn.execute(insert_domain)


def generate_universities():
    for uni in range(40):
        insert_university = university.insert().values(uni_name=fake.company(),
                                                       postal_code=fake.postalcode(),
                                                       town=fake.city(),
                                                       address=fake.address(),
                                                       country=fake.country())
        conn.execute(insert_university)


def generate_users():
    # Select query
    query = 'SELECT university_id from university'

    # Select all universities
    university_ids = conn.execute(query).fetchall()

    for i in range(2000):
        insert_user = user.insert().values(university_id=university_ids[random_from_range(university_ids)][0],
                                           name=fake.first_name(),
                                           surname=fake.last_name(),
                                           email=fake.first_name() + fake.last_name() + '@' + fake.domain_name() + random.randrange(0, 200),
                                           registration_date=date.today())
        conn.execute(insert_user)


def generate_events():
    for i in range(5):
        insert_event = event.insert().values(event_name=fake.name(),
                                             organizing_body=fake.company(),
                                             address=fake.address(),
                                             postal_code=fake.postalcode(),
                                             town=fake.city())
        conn.execute(insert_event)


def generate_tickets():
    for i in range(1500):
        insert_ticket = ticket.insert().values(
            cost=(random.random() * 200),
            purchase_date=date.today())
        conn.execute(insert_ticket)


def generate_welcomepacks():
    query = 'SELECT COUNT(*) from user'

    number_of_welcome_packs = conn.execute(query).fetchone()

    shirt_size = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

    for number in range(number_of_welcome_packs[0]):
        insert_welcomepack = welcomepack.insert().values(shirt_size=shirt_size[random_from_range(shirt_size)])
        conn.execute(insert_welcomepack)


def generate_classrooms():
    for clas in range(30):
        insert_class = classroom.insert().values(classroom_number=randint(1, 700),
                                                 postal_code=fake.postalcode(),
                                                 town=fake.city(), address=fake.address())
        conn.execute(insert_class)


def generate_timetables():
    # Select query
    query = 'SELECT event_id from event'

    # Select all universities
    event_ids = conn.execute(query).fetchall()
    for tt in range(6):
        insert_timetable = timetable.insert().values(event_id=event_ids[random_from_range(event_ids)][0],
                                                     timetable_name=fake.postalcode(),
                                                     date=fake.date_between(start_date="today", end_date='+30d'))
        conn.execute(insert_timetable)


def generate_papers():
    query_participant = 'SELECT user_id from participant'
    user_ids = conn.execute(query_participant).fetchall()

    query_domain = 'SELECT domain_id from domain'
    domain_ids = conn.execute(query_domain).fetchall()

    for i in range(200):
        insert_paper = paper.insert().values(user_id=user_ids[random_from_range(user_ids)][0],
                                             domain_id=domain_ids[random_from_range(domain_ids)][0],
                                             topic=fake.word(ext_word_list=None),
                                             abstrakt=fake.fake.paragraphs(nb=3, ext_word_list=None))
        conn.execute(insert_paper)


def generate_administrators():
    query = 'SELECT user_id from user'

    user_ids = conn.execute(query).fetchall()

    for adm in range(50):
        insert_administrator = administrator.insert().values(user_id=user_ids[random_from_range(user_ids)],
                                                             duty=fake.job())
        conn.execute(insert_administrator)


def generate_reviewers():
    # Select query
    query = 'SELECT user_id from reviewers'

    # Select all universities
    user_ids = conn.execute(query).fetchall()
    for r in range(50):
        insert_reviewers = timetable.insert().values(user_id=user_ids[random_from_range(user_ids)][0],
                                                     academic_title=fake.job)
        conn.execute(insert_reviewers)


def generate_participants():
    welcomepack_query = 'SELECT welcomepack_id from welcomepack'
    welcomepack_ids = conn.execute(welcomepack_query).fetchall()
    shuffle(welcomepack_ids)

    ticket_query = 'SELECT ticket_id from ticket'
    ticket_ids = conn.execute(ticket_query).fetchall()
    shuffle(ticket_ids)

    user_query = 'SELECT user_id from user'
    user_ids = conn.execute(user_query).fetchall()
    shuffle(user_ids)

    for part in range(1500):
        insert_participant = participant.insert().values(
            welcomepack_id=welcomepack_ids[part],
            ticket_id=ticket_ids[part],
            user_id=user_ids[part])

        conn.execute(insert_participant)


def generate_suprevisions():
    query1 = 'SELECT timetable_id from timetable'
    query2 = 'SELECT user_id from administrator'

    user_ids = conn.execute(query2).fetchall()
    timetable_ids = conn.execute(query1).fetchall()
    for i in range(len(timetable_ids)):
        insert_supervision = supervision.insert().values(user_id=user_ids[random_from_range(user_ids)],
                                                         timetable_id=timetable_ids[random_from_range(timetable_ids)])
        conn.execute(insert_supervision)


def generate_grades():
    query = 'SELECT p.paper_id, dr.user_id FROM domain_reviewer dr JOIN paper p on p.domain_id = dr.domain_id'
    paper_user_ids = conn.execute(query).fetchall()
    for i in range(200):
        paper_user = paper_user_ids[random_from_range(paper_user_ids)]
        insert_grade = grade.insert().values(paper_id=paper_user["paper_id"],
                                             user_id=paper_user["user_id"])
        conn.execute(insert_grade)


def generate_domain_reviewers():
    query1 = 'SELECT domain_id from domain'
    query2 = 'SELECT user_id from reviewer'

    domain_ids = conn.execute(query1).fetchall()
    user_ids = conn.execute(query2).fetchall()
    for i in range(230):
        insert_domain_reviewers = supervision.insert().values(user_id=user_ids[random_from_range(user_ids)],
                                                              domain_id=domain_ids[random_from_range(domain_ids)])
        conn.execute(insert_domain_reviewers)


def generate_lectures():
    query1 = 'SELECT classroom_id from classroom'
    query2 = 'SELECT user_id from participant'
    query3 = 'SELECT timetable_id from timetable'
    query4 = 'SELECT paper_id from paper'
    classroom_ids = conn.execute(query1).fetchall()
    user_ids = conn.execute(query2).fetchall()
    timetable_ids = conn.execute(query3).fetchall()
    paper_ids = conn.execute(query4).fetchall()

    for i in range(250):
        insert_lecture = lecture.insert().values(user_id=user_ids[random_from_range(user_ids)],
                                                 classroom_id=classroom_ids[random_from_range(classroom_ids)],
                                                 timetable_id=timetable_ids[random_from_range(timetable_ids)],
                                                 paper_id=paper_ids[random_from_range(paper_ids)],
                                                 start_time=fake.time(),
                                                 duration=random.randrange(45, 90))
        conn.execute(insert_lecture)


def generate_participations():
    query1 = 'SELECT user_id from participant'
    participant_ids = conn.execute(query1).fetchall()

    query2 = 'SELECT lecture_id FROM lecture'
    lecture_ids = conn.execute(query2).fetchall()

    insert_participants = participation.insert().values(user_id=participant_ids[random_from_range(participant_ids)],
                                                        lecture_id=lecture_ids[random_from_range(lecture_ids)])
    conn.execute(insert_participants)


def random_from_range(collection):
    return randrange(len(collection))


# No foreign keys needed #
generate_universities()
generate_events()
generate_tickets()
generate_welcomepacks()
generate_classrooms()
generate_domains()

# User and timetable #
generate_users()
generate_timetables()

# Paper, administrator, reviewer, participant #
generate_participants()
generate_papers()
generate_administrators()
generate_reviewers()

# supervision, grade, domain_reviewer, lecture #
generate_suprevisions()
generate_grades()
generate_domain_reviewers()
generate_lectures()

# participation #
generate_participations()
