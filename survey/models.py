from flask.ext.login import UserMixin


class User(UserMixin):
    def __init__(self, username, password=None):
        self.username = username
        self.password = password


class Survey(object):
    def __init__(self, title, description, is_public=False, survey_id=None):
        self.survey_id = survey_id
        self.title = title
        self.description = description
        self.is_public = is_public


class Question(object):
    def __init__(self, title, question, answer, possibilities, survey_id, question_id=None):
        self.title = title
        self.question = question
        self.answer = answer
        self.possibilities = possibilities
        self.survey_id = survey_id
        self.question_id = question_id


class Answer(object):
    def __init__(self, answer_type, answer_content, question_id, answer_id=None):
        self.answer_type = answer_type
        self.answer_content = answer_content
        self.question_id = question_id
        self.answer_id = answer_id
