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
    responses = session.get(RESPONSES_KEY)
    if (responses is None):
        # trying to access question page too soon
        return redirect('/')
    if (len(responses) == len(question_list)):
        # make sure user won't be able to access previous questions once they finish the survey
        return redirect("/thanks")
    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"The question that you're requesting doesn't exist", 'skip_question')
        return redirect(f"/questions/{len(responses)}")
    current_question = question_list[qid].question
    current_choice_0 = question_list[qid].choices[0]
    current_choice_1 = question_list[qid].choices[1]
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
    else:
        return redirect('/thanks')


# fruits = session['fruits']
# # reading
# fruits.append('new item')
# # updating
# session['fruits'] = fruits
# # re-save the data

# session['fruits'] = session['fruits'] + ['cherry']
# # updating/saving


# session['fruits'] reading the data
