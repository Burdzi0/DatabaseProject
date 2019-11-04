from datetime import date
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Time
from faker import Faker
from random import randrange

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

conn = engine.connect()
fake = Faker()


def generate_domain():
    for dom in range(20):
        insert_domain = domain.insert().values(domain_name=fake.job())
        conn.execute(insert_domain)


generate_domain()


def generate_universities():
    for uni in range(40):
        insert_university = university.insert().values(uni_name=fake.company(),
                                                       postal_code=fake.postalcode(),
                                                       town=fake.city(),
                                                       address=fake.address(),
                                                       country=fake.country())
        conn.execute(insert_university)


# Create university
generate_universities()


def random_university(university_ids):
    return randrange(len(university_ids))


def generate_users():
    # Select query
    query = 'SELECT university_id from university'

    # Select all universities
    university_ids = conn.execute(query).fetchall()

    for i in range(2000):
        insert_user = user.insert().values(university_id=university_ids[random_university(university_ids)][0],
                                           name=fake.first_name(),
                                           surname=fake.last_name(),
                                           email=fake.first_name() + fake.last_name() + '@' + fake.domain_name(),
                                           registration_date=date.today())
        conn.execute(insert_user)


generate_users()
