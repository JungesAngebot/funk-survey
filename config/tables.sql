DROP SCHEMA IF EXISTS bl_survey CASCADE;
CREATE SCHEMA bl_survey;

create TYPE bl_survey.answer_type as ENUM ('single_choice', 'multiple_choice', 'textual', 'rank');

create table bl_survey.user (
  id serial PRIMARY KEY not NULL,
  username text not null,
  password text not null
);

create table bl_survey.survey (
  id serial PRIMARY KEY not null,
  title text,
  description text,
  is_public boolean DEFAULT false
);

create table bl_survey.question (
  id serial PRIMARY KEY not null,
  title text,
  question text,
  answer bl_survey.answer_type,
  possibilities text,
  survey_id int
);

create TABLE bl_survey.answer (
  id serial PRIMARY KEY not null,
  answer_type bl_survey.answer_type,
  answer_content text,
  question_id int
);

insert into bl_survey.user (username, password) VALUES ('admin', '7dd12f3a9afa0282a575b8ef99dea2a0c1becb51');
insert into bl_survey.user (username, password) VALUES ('test', '5e52fee47e6b070565f74372468cdc699de89107');

