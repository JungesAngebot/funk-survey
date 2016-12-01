import hashlib

from commonspy.logging import log_info, log_error
from flask import redirect
from flask import render_template, session
from flask import request
from flask import url_for
from flask.ext.login import login_required

from survey import login_manager
from survey.blueprints import app
from survey.db import *
from survey.models import User, Survey, Question, Answer, SurveyResult


@login_manager.request_loader
def load_user(request):
    if 'user' in session:
        return User(session.get('user'))
    h = hashlib.new('ripemd160')
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    if username is None or password is None:
        return None
    h.update(password.encode())
    user = get_user_by_name(username)
    if user is None:
        return None
    if user.password != h.hexdigest():
        return None
    session['user'] = user.username
    return user


@app.route('/')
def index_page():
    return render_template('index/default.html', surveys=get_surveys_by_visibility())


@app.route('/login')
def admin_login_page():
    return render_template('admin/login.html')


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_page():
    return render_template('admin/admin.html', page='admin', surveys=get_surveys())


@app.route('/admin/create_survey', methods=['GET', 'POST'])
@login_required
def create_survey():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        is_public = request.form.get('is_public', False)
        create_new_survey(Survey(title, description, is_public))
    return render_template('admin/create_survey.html', page='create_survey')


@app.route('/admin/user_management')
@login_required
def user_management():
    return render_template('admin/user_management.html', page='user_management', users=get_all_users())


@app.route('/admin/user_management/<string:username>', methods=['GET', 'POST'])
@login_required
def user_detail_page(username):
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        h = hashlib.new('ripemd160')
        h.update(password.encode())
        password = h.hexdigest()
        update_user_by_name(User(username, password), session.get('user'))
        session['user'] = username
    return render_template('admin/user_detail.html', page='user_management', user=get_user_by_name(username))


@app.route('/admin/user_management/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        h = hashlib.new('ripemd160')
        h.update(password.encode())
        password = h.hexdigest()
        create_new_user(username, password)
    return render_template('admin/create_user.html', page='user_management')


@app.route('/admin/user_management/delete/<string:username>')
@login_required
def delete_user(username):
    delete_user_by_name(username)
    return redirect(url_for('handler.user_management'))


@app.route('/survey/<string:survey_id>', methods=['GET', 'POST'])
@login_required
def view_survey(survey_id):
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        is_public = request.form.get('is_public')
        update_survey(Survey(title, description, is_public, survey_id))
    return render_template('admin/survey_detail_view.html', survey=get_survey_by_id(survey_id))


@app.route('/survey/delete/<string:survey_id>')
@login_required
def delete_survey(survey_id):
    delete_survey_by_id(survey_id)
    return redirect(url_for('handler.admin_page'))


@app.route('/questions')
@login_required
def questions():
    return render_template('admin/questions.html', page='questions', questions=get_all_questions())


@app.route('/questions/create', methods=['GET', 'POST'])
@login_required
def create_question():
    if request.method == 'POST':
        title = request.form.get('title')
        question = request.form.get('question')
        answer = request.form.get('answer', 'single_choice')
        possibilities = request.form.get('possibilities')
        survey_id = request.form.get('survey_id')
        create_new_question(Question(title, question, answer, possibilities, survey_id))
    return render_template('admin/question_create.html', surveys=get_surveys())


@app.route('/questions/<string:question_id>', methods=['GET', 'POST'])
@login_required
def view_question(question_id):
    if request.method == 'POST':
        title = request.form.get('title')
        question = request.form.get('question')
        answer = request.form.get('answer')
        possibilities = request.form.get('possibilities')
        survey_id = request.form.get('survey_id')
        update_question(Question(title, question, answer, possibilities, survey_id, question_id))

    return render_template('admin/show_results_for_single_question.html', question=get_question_by_id(question_id))


@app.route('/questions/delete/<string:question_id>')
@login_required
def delete_question_by_question_id(question_id):
    delete_question(question_id)
    return redirect(url_for('handler.questions'))


@app.route('/participate/survey/<string:survey_id>', methods=['GET', 'POST'])
def show_survey_for_participants(survey_id):
    if request.method == 'POST':
        questions = get_questions_by_survey_id(survey_id)
        answers = list()
        for question in questions:
            log_info('Question: %s' % question.title)
            question_id = question.question_id
            if question.answer == 'multiple_choice':
                values = []
                for key, value in request.form.items():
                    if key.startswith(str(question_id)):
                        values.append('%s|%s' % (key, value))
                answers.append(Answer(question.answer, ','.join(values), question.question_id))
            else:
                for key, value in request.form.items():
                    if key.startswith(str(question_id)):
                        answers.append(Answer(question.answer, '%s|%s' % (key, value), question.question_id))
        save_answers(answers)

        participant_name = request.form.get('participantName')
        partner_manager = request.form.get('participantManager')
        department = request.form.get('participantDepartment')
        creator_format = request.form.get('creatorName')
        save_survey_fields(SurveyResult(participant_name, partner_manager, department, creator_format, survey_id))
        log_info('Survey submitted')

    return render_template('survey/participate.html', survey=get_survey_by_id(survey_id),
                           questions=get_questions_by_survey_id(survey_id),
                           creators=get_creators_from_business_layer_table())


@app.route('/results')
@login_required
def result_overview():
    return render_template('admin/survey_result_overview.html', page='result', surveys=get_surveys())


@app.route('/results/<string:survey_id>')
@login_required
def show_results_for_survey(survey_id):
    return render_template('admin/show_results_for_survey.html', page='result', survey=get_survey_by_id(survey_id),
                           questions=get_questions_by_survey_id(survey_id))


@app.route('/results/<string:survey_id>/<string:question_id>')
@login_required
def show_results_for_single_question(survey_id, question_id):
    results = get_answers_by_question_id(question_id)
    rendered_results = []
    question = get_question_by_id(question_id)
    question.yes_count = 0
    question.no_count = 0
    data = {}
    for p in question.possibilities.split(','):
        data[p] = 0
    for answer in results:
        if answer.answer_type == 'single_choice':
            if 'yes' in answer.answer_content:
                answer.answer_content = 'Yes for: %s' % get_question_by_id(answer.question_id).question
                question.yes_count += 1
            else:
                answer.answer_content = 'No for: %s' % get_question_by_id(answer.question_id).question
                question.no_count += 1
        elif answer.answer_type == 'multiple_choice':
            r = []
            for selection in answer.answer_content.split(','):
                value = selection.split('|')[0]
                qid, idx = value.split('_')
                question = get_question_by_id(question_id)
                possibilities = question.possibilities.split(',')
                r.append(possibilities[int(idx) - 1])
            for value in r:
                data[value] += 1

            answer.answer_content = '%s: %s' % (get_question_by_id(question_id).question, ','.join(r))
        else:
            answer.answer_content = '%s: %s' % (
                get_question_by_id(answer.question_id).question, answer.answer_content.split('|')[1])
        rendered_results.append(answer)
    return render_template('admin/show_results_for_single_question.html', page='result',
                           question=question, answers=rendered_results, survey_id=survey_id,
                           possibilities=[p.strip().replace("'", '') for p in question.possibilities.split(',')],
                           data=data)


@app.errorhandler(Exception)
def exception_handler(e):
    log_error(e)
    return render_template('error/error.html')
