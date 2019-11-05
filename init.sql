/*
drop table user;

drop table university;

drop table participant;

drop table welcomepack;

drop table ticket;

drop table lecture;

drop table particiption;

drop table classroom;

drop table timetable;

drop table domain;

drop table paper;

drop table reviewer;

drop table grade;

drop table administrator;

drop table event;

drop table supervision;

drop table domain_reviewer;
*/


CREATE TABLE "user" (
    "user_id" serial NOT NULL,
    "university_id" integer NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "surname" VARCHAR(70) NOT NULL,
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "registration_date" DATE NOT NULL,
    CONSTRAINT "user_pk" PRIMARY KEY ("user_id")
);


CREATE TABLE "university" (
    "university_id" serial NOT NULL,
    "uni_name" VARCHAR(50) NOT NULL,
    "postal_code" VARCHAR(10) NOT NULL,
    "town" VARCHAR(100) NOT NULL,
    "address" VARCHAR(100) NOT NULL,
    "country" VARCHAR(50) NOT NULL,
    CONSTRAINT "university_pk" PRIMARY KEY ("university_id")
);



CREATE TABLE "participant" (
    "welcomepack_id" integer UNIQUE,
    "ticket_id" integer UNIQUE,
    "user_id" integer NOT NULL,
    CONSTRAINT "participant_pk" PRIMARY KEY ("user_id")
);



CREATE TABLE "welcomepack" (
    "welcomepack_id" serial NOT NULL,
    "shirt_size" VARCHAR(5) NOT NULL,
    CONSTRAINT "welcomepack_pk" PRIMARY KEY ("welcomepack_id")
);



CREATE TABLE "ticket" (
    "ticket_id" serial NOT NULL,
    "cost" FLOAT NOT NULL CONSTRAINT ticket_cost_more_than_zero CHECK (cost > 0),
    "purchase_date" DATE NOT NULL,
    CONSTRAINT "ticket_pk" PRIMARY KEY ("ticket_id")
);



CREATE TABLE "lecture" (
    "lecture_id" serial NOT NULL,
    "user_id" integer NOT NULL,
    "classroom_id" integer NOT NULL,
    "timetable_id" integer,
    "paper_id" integer NOT NULL,
    "start_time" TIME NOT NULL,
    "duration" TIMESTAMP NOT NULL,
    CONSTRAINT "lecture_pk" PRIMARY KEY ("lecture_id")
);



CREATE TABLE "participation" (
    "user_id" integer NOT NULL,
    "lecture_id" integer NOT NULL,
    CONSTRAINT "participation_pk" PRIMARY KEY ("user_id","lecture_id")
);



CREATE TABLE "classroom" (
    "classroom_id" serial NOT NULL,
    "classroom_number" integer NOT NULL CONSTRAINT classroom_number_over_zero CHECK (classroom_number > 0),
    "postal_code" VARCHAR(10) NOT NULL,
    "town" VARCHAR(100) NOT NULL,
    "address" VARCHAR(100) NOT NULL,
    CONSTRAINT "classroom_pk" PRIMARY KEY ("classroom_id")
);



CREATE TABLE "timetable" (
    "timetable_id" serial NOT NULL,
    "event_id" integer NOT NULL,
    "timetable_name" VARCHAR(50) NOT NULL,
    "date" DATE NOT NULL,
    CONSTRAINT "timetable_pk" PRIMARY KEY ("timetable_id")
);



CREATE TABLE "domain" (
    "domain_id" serial NOT NULL,
    "domain_name" VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT "domain_pk" PRIMARY KEY ("domain_id")
);



CREATE TABLE "paper" (
    "paper_id" serial NOT NULL,
    "user_id" integer NOT NULL,
    "domain_id" integer NOT NULL,
    "topic" VARCHAR(100) NOT NULL,
    "abstrakt" TEXT NOT NULL,
    CONSTRAINT "paper_pk" PRIMARY KEY ("paper_id")
);



CREATE TABLE "reviewer" (
    "user_id" integer NOT NULL,
    "academic_title" VARCHAR(100) NOT NULL,
    CONSTRAINT "reviewer_pk" PRIMARY KEY ("user_id")
);



CREATE TABLE "grade" (
    "paper_id" integer NOT NULL,
    "user_id" serial NOT NULL,
    "grade" FLOAT NOT NULL CONSTRAINT grade_more_than_zero CHECK (grade>0 AND grade <=10),
    "reason" TEXT NOT NULL,
    CONSTRAINT "grade_pk" PRIMARY KEY ("paper_id","user_id")
);



CREATE TABLE "administrator" (
    "user_id" integer NOT NULL,
    "duty" VARCHAR(100) NOT NULL,
    CONSTRAINT "administrator_pk" PRIMARY KEY ("user_id")
);



CREATE TABLE "event" (
    "event_id" serial NOT NULL,
    "event_name" VARCHAR(100) NOT NULL,
    "organizing_body" VARCHAR(100) NOT NULL,
    "address" VARCHAR(100) NOT NULL,
    "postal_code" VARCHAR(10) NOT NULL,
    "town" VARCHAR(100) NOT NULL,
    CONSTRAINT "event_pk" PRIMARY KEY ("event_id")
);



CREATE TABLE "supervision" (
    "user_id" serial NOT NULL,
    "timetable_id" integer NOT NULL,
    CONSTRAINT "supervision_pk" PRIMARY KEY ("user_id","timetable_id")
);



CREATE TABLE "domain_reviewer" (
    "user_id" integer NOT NULL,
    "domain_id" integer NOT NULL,
    CONSTRAINT "domain_reviewer_pk" PRIMARY KEY ("user_id","domain_id")
);



ALTER TABLE "user" ADD CONSTRAINT "user_fk0" FOREIGN KEY ("university_id") REFERENCES "university"("university_id");

ALTER TABLE "participant" ADD CONSTRAINT "participant_fk0" FOREIGN KEY ("welcomepack_id") REFERENCES "welcomepack"("welcomepack_id");

ALTER TABLE "participant" ADD CONSTRAINT "participant_fk1" FOREIGN KEY ("ticket_id") REFERENCES "ticket"("ticket_id");

ALTER TABLE "participant" ADD CONSTRAINT "participant_fk2" FOREIGN KEY ("user_id") REFERENCES "user"("user_id")
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "lecture" ADD CONSTRAINT "lecture_fk1" FOREIGN KEY ("classroom_id") REFERENCES "classroom"("classroom_id");

ALTER TABLE "lecture" ADD CONSTRAINT "lecture_fk2" FOREIGN KEY ("timetable_id") REFERENCES "timetable"("timetable_id");

ALTER TABLE "lecture" ADD CONSTRAINT "lecture_fk3" FOREIGN KEY ("paper_id") REFERENCES "paper"("paper_id")
ON DELETE CASCADE;

ALTER TABLE "participation" ADD CONSTRAINT "participation_fk0" FOREIGN KEY ("user_id") REFERENCES "participant"("user_id")
ON DELETE CASCADE;

ALTER TABLE "participation" ADD CONSTRAINT "participation_fk1" FOREIGN KEY ("lecture_id") REFERENCES "lecture"("lecture_id")
ON DELETE CASCADE;

ALTER TABLE "timetable" ADD CONSTRAINT "timetable_fk0" FOREIGN KEY ("event_id") REFERENCES "event"("event_id");

ALTER TABLE "paper" ADD CONSTRAINT "paper_fk0" FOREIGN KEY ("user_id") REFERENCES "participant"("user_id")
ON DELETE CASCADE;

ALTER TABLE "paper" ADD CONSTRAINT "paper_fk1" FOREIGN KEY ("domain_id") REFERENCES "domain"("domain_id");

ALTER TABLE "reviewer" ADD CONSTRAINT "reviewer_fk0" FOREIGN KEY ("user_id") REFERENCES "user"("user_id")
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "grade" ADD CONSTRAINT "grade_fk0" FOREIGN KEY ("paper_id") REFERENCES "paper"("paper_id")
ON UPDATE CASCADE;

ALTER TABLE "grade" ADD CONSTRAINT "grade_fk1" FOREIGN KEY ("user_id") REFERENCES "reviewer"("user_id")
ON DELETE CASCADE;

ALTER TABLE "administrator" ADD CONSTRAINT "administrator_fk0" FOREIGN KEY ("user_id") REFERENCES "user"("user_id")
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "supervision" ADD CONSTRAINT "supervision_fk0" FOREIGN KEY ("user_id") REFERENCES "administrator"("user_id")
ON DELETE CASCADE;

ALTER TABLE "supervision" ADD CONSTRAINT "supervision_fk1" FOREIGN KEY ("timetable_id") REFERENCES "timetable"("timetable_id");

ALTER TABLE "domain_reviewer" ADD CONSTRAINT "domain_reviewer_fk0" FOREIGN KEY ("user_id") REFERENCES "reviewer"("user_id")
ON DELETE CASCADE;

ALTER TABLE "domain_reviewer" ADD CONSTRAINT "domain_reviewer_fk1" FOREIGN KEY ("domain_id") REFERENCES "domain"("domain_id");
