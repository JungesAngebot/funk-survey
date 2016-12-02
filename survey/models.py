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


class SurveyResult(object):
    def __init__(self, participant_name, manager, department, creator_format, survey_id, survey_completed_id=None):
        self.participant_name = participant_name
        self.manager = manager
        self.department = department
        self.format = creator_format
        self.survey_id = survey_id
        self.survey_completed_id = survey_completed_id


class Question(object):
    def __init__(self, title, question, answer, possibilities, metric, platform, time_frame,
                 survey_id, question_id=None):
        self.title = title
        self.question = question
        self.answer = answer
        self.possibilities = possibilities
        self.survey_id = survey_id
        self.metric = metric
        self.platform = platform
        self.time_frame = time_frame
        self.question_id = question_id


class Answer(object):
    def __init__(self, answer_type, answer_content, question_id, answer_id=None):
        self.answer_type = answer_type
        self.answer_content = answer_content
        self.question_id = question_id
        self.answer_id = answer_id


class Creator(object):
    def __init__(self, creator_format):
        self.format_name = creator_format
