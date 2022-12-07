from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
"""turn the redicrect message off"""
debug = DebugToolbarExtension(app)

responses = []
title = satisfaction_survey.title
instructions = satisfaction_survey.instructions
question_list = satisfaction_survey.questions


@app.route('/')
def survey_questions():
    return render_template('start.html', title=title, instructions=instructions)


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
    responses.append(current_answer)
    if len(responses) < len(question_list):
        return redirect(f"/questions/{len(responses)}")
    elif len(responses) == len(question_list):
        return redirect('/thanks')
    else:
        flash('please continue the survey where you stopped :)')
    # return render_template('thanks.html', responses=responses)
