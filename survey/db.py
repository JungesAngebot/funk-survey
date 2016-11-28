import psycopg2 as pg
import psycopg2.extras as pgextra

from survey import config
from survey.models import User, Survey, Question, Answer


def create_connection():
    return pg.connect(
        host=config.property('database.host'),
        port=config.property('database.port'),
        dbname=config.property('database.database_name'),
        user=config.property('database.username'),
        password=config.property('database.password'),
        cursor_factory=pgextra.RealDictCursor,
        connect_timeout=config.property('database.connection_timeout')
    )


def get_surveys():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('select * from bl_survey.survey')
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return [Survey(row.get('title'), row.get('description'), row.get('is_public'), row.get('id')) for row in rows]


def get_surveys_by_visibility(is_public=True):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('select * from bl_survey.survey where is_public = %s', (is_public,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return [Survey(row.get('title'), row.get('description'), row.get('is_public'), row.get('id')) for row in rows]


def get_user_by_name(username):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('select username, password from bl_survey.user where username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return User(user.get('username'), user.get('password'))


def get_all_users():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('select username, password from bl_survey.user')
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return [User(user.get('username'), user.get('password')) for user in users]


def update_user_by_name(user, original_username):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('update bl_survey.user set username = %s, password = %s where username = %s',
                   (user.username, user.password, original_username))
    connection.commit()
    cursor.close()
    connection.close()


def create_new_user(username, password):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('insert into bl_survey.user (username, password) values(%s, %s)', (username, password))
    connection.commit()
    cursor.close()
    connection.close()


def delete_user_by_name(username):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('delete from bl_survey.user where username = %s', (username,))
    connection.commit()
    cursor.close()
    connection.close()


def create_new_survey(survey):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('insert into bl_survey.survey (title, description, is_public) values (%s, %s, %s)',
                   (survey.title, survey.description, survey.is_public))
    connection.commit()
    cursor.close()
    connection.close()


def get_survey_by_id(survey_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('select * from bl_survey.survey where id = %s', (survey_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return Survey(row.get('title'), row.get('description'), row.get('is_public'), row.get('id'))


def update_survey(survey):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('update bl_survey.survey set title = %s, description = %s, is_public = %s where id = %s',
                   (survey.title, survey.description, survey.is_public, survey.survey_id))
    connection.commit()
    cursor.close()
    connection.close()


def delete_survey_by_id(survey_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('delete from bl_survey.survey where id = %s', (survey_id,))
    connection.commit()
    cursor.close()
    connection.close()


def create_new_question(question):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        'insert into bl_survey.question (title, question, answer, possibilities, survey_id) values (%s, %s, %s, %s, %s)'
        , (question.title, question.question, question.answer, question.possibilities, question.survey_id))
    connection.commit()
    cursor.close()
    connection.close()


def update_question(question):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        'update bl_survey.question set title = %s, question = %s, answer = %s, possibilities = %s, survey_id = %s '
        'where id = %s',
        (question.title, question.question, question.answer, question.possibilities, question.survey_id,
         question.question_id))
    connection.commit()
    cursor.close()
    connection.close()


def delete_question(question_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('delete from bl_survey.question where id = %s', (question_id,))
    connection.commit()
    cursor.close()
    connection.close()


def get_question_by_id(question_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('select * from bl_survey.question where id = %s', (question_id,))
    row = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return Question(row.get('title'), row.get('question'), row.get('answer'), row.get('possibilities'),
                    row.get('survey_id'), row.get('id'))


def get_questions_by_survey_id(survey_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('select * from bl_survey.question where survey_id = %s', (survey_id,))
    rows = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return [Question(row.get('title'), row.get('question'), row.get('answer'), row.get('possibilities'),
                     row.get('survey_id'), row.get('id')) for row in rows]


def get_all_questions():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('select * from bl_survey.question')
    rows = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return [Question(row.get('title'), row.get('description'), row.get('answer'), row.get('possibilities'),
                     row.get('survey_id'), row.get('id')) for row in rows]


def save_answers(answers):
    connection = create_connection()
    cursor = connection.cursor()
    for answer in answers:
        cursor.execute('insert into bl_survey.answer (answer_type, answer_content, question_id) values (%s, %s, %s)',
                       (answer.answer_type, answer.answer_content, answer.question_id))
    connection.commit()
    cursor.close()
    connection.close()


def get_answers_by_question_id(question_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('select * from bl_survey.answer where question_id = %s', (question_id,))
    rows = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return [Answer(row.get('answer_type'), row.get('answer_content'), row.get('question_id')) for row in rows]
