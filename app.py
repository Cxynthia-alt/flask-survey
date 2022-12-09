from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
"""turn the redicrect message off"""
debug = DebugToolbarExtension(app)


title = satisfaction_survey.title
instructions = satisfaction_survey.instructions
question_list = satisfaction_survey.questions


@app.route('/')
def show_survey():
    return render_template('start.html', title=title, instructions=instructions)


@app.route("/begin", methods=['POST'])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')


@app.route('/questions/<int:qid>')
def questions(qid):

    current_question = question_list[qid].question
    current_choice_0 = question_list[qid].choices[0]
    current_choice_1 = question_list[qid].choices[1]
    if (qid > len(question_list)):
        flash('This is not part of the question, please continue the survey where you stopped :)')
    else:
        return render_template('questions.html', current_question=current_question, qid=qid, current_choice_0=current_choice_0, current_choice_1=current_choice_1)


@app.route('/thanks')
def thank_you_page():
    return render_template('thanks.html')


@app.route('/answer', methods=['POST'])
def collect_answer():
    current_answer = request.form['options']
    responses = session[RESPONSES_KEY]
    responses.append(current_answer)
    session[RESPONSES_KEY] = responses
    if len(responses) < len(question_list):
        return redirect(f"/questions/{len(responses)}")
    elif len(responses) == len(question_list):
        return redirect('/thanks')
    else:
        flash('please continue the survey where you stopped :)')
    # return render_template('thanks.html', responses=responses)


# fruits = session['fruits']
# # reading
# fruits.append('new item')
# # updating
# session['fruits'] = fruits
# # re-save the data

# session['fruits'] = session['fruits'] + ['cherry']
# # updating/saving


# session['fruits'] reading the data
