import random
from datetime import date
from random import randrange, randint

from faker import Faker
from faker.providers.job import Provider
from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Time, Float
from sqlalchemy import create_engine

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
    domains = list(set(Provider.jobs))

    for dom in range(20):
        print_status("domain", dom)
        insert_domain = domain.insert().values(domain_name=domains[dom][:50])
        conn.execute(insert_domain)


def generate_universities():
    for uni in range(40):
        print_status("university", uni)
        try_insert_without_parameters(create_university_query)


def print_status(name, number):
    print("Generating {} {}".format(name, number), end="\r")


def create_university_query():
    return university.insert().values(uni_name=fake.company(),
                                      postal_code=fake.postalcode(),
                                      town=fake.city(),
                                      address=fake.address()[:100],
                                      country=fake.country()[:50])


def generate_users():
    # Select query
    query = 'SELECT university_id from university'

    # Select all universities
    university_ids = conn.execute(query).fetchall()

    for i in range(3000):
        print_status("user", i)
        try_insert(create_users_query, university_ids)


def create_users_query(*args):
    university_ids = args[0]
    insert_user = user.insert().values(university_id=university_ids[random_from_range(university_ids)][0],
                                       name=fake.first_name(),
                                       surname=fake.last_name(),
                                       email=fake.first_name() + fake.last_name() + str(random.randrange(0, 200))
                                                                                        + '@' + fake.domain_name(),
                                       registration_date=date.today())
    return insert_user


def generate_events():
    for i in range(5):
        print_status("event", i)
        try_insert_without_parameters(create_events_query)


def create_events_query():
    insert_event = event.insert().values(event_name=fake.name(),
                                         organizing_body=fake.company(),
                                         address=fake.address(),
                                         postal_code=fake.postalcode(),
                                         town=fake.city())
    return insert_event


def generate_tickets():
    for i in range(1500):
        print_status("ticket", i)
        try_insert_without_parameters(create_ticket_query)


def create_ticket_query():
    insert_ticket = ticket.insert().values(
        cost=(random.random() * 200),
        purchase_date=date.today())
    return insert_ticket


def generate_welcomepacks():
    number_of_welcome_packs = 5000

    shirt_size = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

    for number in range(number_of_welcome_packs):
        print_status("welcomepack", number)
        try_insert(create_welcomepack_query, shirt_size)

    print(conn.execute('SELECT COUNT(*) from welcomepack').fetchone())


def create_welcomepack_query(shirt_size):
    shirt = shirt_size[random_from_range(shirt_size)]
    return welcomepack.insert().values(shirt_size=shirt)


def generate_classrooms():
    for clas in range(30):
        print_status("classroom", clas)
        try_insert_without_parameters(create_classroom_query)


def create_classroom_query():
    insert_class = classroom.insert().values(classroom_number=randint(1, 700),
                                             postal_code=fake.postalcode(),
                                             town=fake.city(), address=fake.address())
    return insert_class


def generate_timetables():
    # Select query
    query = 'SELECT event_id from event'

    # Select all universities
    event_ids = conn.execute(query).fetchall()
    for tt in range(6):
        print_status("timetable", tt)
        try_insert(create_timetable_query, event_ids)


def create_timetable_query(event_ids):
    insert_timetable = timetable.insert().values(event_id=event_ids[random_from_range(event_ids)][0],
                                                 timetable_name=fake.postalcode(),
                                                 date=fake.date_between(start_date="today", end_date='+30d'))
    return insert_timetable


def generate_papers():
    query_participant = 'SELECT user_id from participant'
    user_ids = conn.execute(query_participant).fetchall()

    query_domain = 'SELECT domain_id from domain'
    domain_ids = conn.execute(query_domain).fetchall()

    for i in range(200):
        print_status("paper", i)
        try_insert(create_paper_query, domain_ids, user_ids)


def create_paper_query(domain_ids, user_ids):
    insert_paper = paper.insert().values(user_id=user_ids[random_from_range(user_ids)][0],
                                         domain_id=domain_ids[random_from_range(domain_ids)][0],
                                         topic=fake.word(ext_word_list=None),
                                         abstrakt=fake.paragraphs(nb=3, ext_word_list=None))
    return insert_paper


def generate_administrators():
    query = 'SELECT user_id from "user"'

    user_ids = conn.execute(query).fetchall()

    for adm in range(50):
        print_status("administrator", adm)
        try_insert(create_administrators_query, user_ids)


def create_administrators_query(user_ids):
    insert_administrator = administrator.insert().values(user_id=user_ids[random_from_range(user_ids)][0],
                                                         duty=fake.job() + str(randrange(500)))
    return insert_administrator


def generate_reviewers():
    query = 'SELECT user_id from "user"'

    user_ids = conn.execute(query).fetchall()

    for r in range(50):
        print_status("reviewer", r)
        try_insert(create_reviewers_query, user_ids)


def create_reviewers_query(user_ids):
    insert_reviewers = reviewer.insert().values(user_id=user_ids[random_from_range(user_ids)][0],
                                                academic_title=fake.job() + str(randrange(500)))
    return insert_reviewers


def generate_participants():
    welcomepack_query = 'SELECT welcomepack_id from welcomepack'
    welcomepack_ids = conn.execute(welcomepack_query).fetchall()

    ticket_query = 'SELECT ticket_id from ticket'
    ticket_ids = conn.execute(ticket_query).fetchall()

    user_query = 'SELECT user_id from "user"'
    user_ids = conn.execute(user_query).fetchall()

    for part in range(1500):
        print_status("participant", part)
        try_insert(create_participant_query, ticket_ids, user_ids, welcomepack_ids)


def create_participant_query(ticket_ids, user_ids, welcomepack_ids):
    insert_participant = participant.insert().values(
        welcomepack_id=welcomepack_ids[random_from_range(welcomepack_ids)][0],
        ticket_id=ticket_ids[random_from_range(ticket_ids)][0],
        user_id=user_ids[random_from_range(user_ids)][0])
    return insert_participant


def generate_suprevisions():
    query1 = 'SELECT timetable_id from timetable'
    query2 = 'SELECT user_id from administrator'

    user_ids = conn.execute(query2).fetchall()
    timetable_ids = conn.execute(query1).fetchall()

    for i in range(len(timetable_ids)):
        print_status("supervision", i)
        try_insert(create_supervision_query, timetable_ids, user_ids)


def create_supervision_query(timetable_ids, user_ids):
    insert_supervision = supervision.insert().values(user_id=user_ids[random_from_range(user_ids)][0],
                                                     timetable_id=timetable_ids[random_from_range(timetable_ids)][0])
    return insert_supervision


def generate_grades():
    query = 'SELECT p.paper_id, dr.user_id FROM domain_reviewer dr JOIN paper p on p.domain_id = dr.domain_id'
    paper_user_ids = conn.execute(query).fetchall()
    for i in range(200):
        print_status("grade", i)
        try_insert(create_grade_query, paper_user_ids)


def create_grade_query(paper_user_ids):
    paper_user = paper_user_ids[random_from_range(paper_user_ids)]
    insert_grade = grade.insert().values(paper_id=paper_user["paper_id"],
                                         user_id=paper_user["user_id"],
                                         grade=round(random.uniform(1.0, 10.0), 2),
                                         reason=fake.sentences(nb=3, ext_word_list=None))
    return insert_grade


def generate_domain_reviewers():
    query1 = 'SELECT domain_id from domain'
    query2 = 'SELECT user_id from reviewer'

    domain_ids = conn.execute(query1).fetchall()
    user_ids = conn.execute(query2).fetchall()
    for i in range(230):
        print_status("domain_reviewer", i)
        try_insert(create_domain_reviewers_query, domain_ids, user_ids)


def create_domain_reviewers_query(domain_ids, user_ids):
    insert_domain_reviewers = domain_reviewer.insert().values(user_id=user_ids[random_from_range(user_ids)][0],
                                                          domain_id=domain_ids[random_from_range(domain_ids)][0])
    return insert_domain_reviewers


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
        print_status("lecture", i)
        try_insert(create_lecture_query, classroom_ids, paper_ids, timetable_ids, user_ids)


def create_lecture_query(classroom_ids, paper_ids, timetable_ids, user_ids):
    insert_lecture = lecture.insert().values(user_id=user_ids[random_from_range(user_ids)][0],
                                             classroom_id=classroom_ids[random_from_range(classroom_ids)][0],
                                             timetable_id=timetable_ids[random_from_range(timetable_ids)][0],
                                             paper_id=paper_ids[random_from_range(paper_ids)][0],
                                             start_time=fake.time(),
                                             duration=random.randrange(45, 90))
    return insert_lecture


def generate_participations():
    query1 = 'SELECT user_id from participant'
    participant_ids = conn.execute(query1).fetchall()

    query2 = 'SELECT lecture_id FROM lecture'
    lecture_ids = conn.execute(query2).fetchall()

    for i in range(len(participant_ids)):
        print_status("participations", i)
        try_insert(create_participants_query, lecture_ids, participant_ids)


def create_participants_query(lecture_ids, participant_ids):
    insert_participants = participation.insert().values(user_id=participant_ids[random_from_range(participant_ids)][0],
                                                        lecture_id=lecture_ids[random_from_range(lecture_ids)][0])
    return insert_participants


def random_from_range(collection):
    return randrange(len(collection))


def try_insert(create_query, *args):
    inserted = False
    query = create_query(*args)
    while not inserted:
        try:
            conn.execute(query)
            inserted = True
        except Exception:
            query = create_query(*args)


def try_insert_without_parameters(create_query):
    inserted = False
    query = create_query()
    while not inserted:
        try:
            conn.execute(query)
            inserted = True
        except Exception:
            query = create_query()


# No foreign keys needed #
generate_universities()
generate_events()
generate_tickets()
generate_welcomepacks()
generate_classrooms()
generate_domains()
#
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
generate_domain_reviewers()
generate_grades()
generate_lectures()

# participation #
generate_participations()
