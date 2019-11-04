from datetime import date
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, Date

meta = MetaData()

engine = create_engine('postgres://docker:docker@localhost/docker', echo=True)

meta.create_all(engine)

# CREATE TABLE "university" (
#     "university_id" serial NOT NULL,
#     "uni_name" VARCHAR(50) NOT NULL,
#     "postal_code" VARCHAR(10) NOT NULL,
#     "town" VARCHAR(100) NOT NULL,
#     "address" VARCHAR(100) NOT NULL,
#     "country" VARCHAR(50) NOT NULL,
#     CONSTRAINT "university_pk" PRIMARY KEY ("university_id")
# );

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

conn = engine.connect()

# Create university
insert_university = university.insert().values(uni_name='PWr', postal_code='50-353', town='Wrocław', address='Address', country='Poland')

# Insert university
conn.execute(insert_university)

# Select query
query = 'SELECT university_id from university'

# Select all universities
university_ids = conn.execute(query).fetchall()

for row in university_ids:
    print(row[0])

insert_user = user.insert().values(university_id=university_ids[0][0], name='Ravi', surname='Surname', email='a@a.com', registration_date=date.today())

conn.execute(insert_user)
