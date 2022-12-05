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


@app.route('/questions')
def survey_questions():
    return render_template('start.html', title=title, instructions=instructions)


@app.route('/questions/0')
def question_0():
    return render_template('question_0.html', question_list=question_list)


@app.route('/questions/1')
def question_1():
    return render_template('question_1.html', question_list=question_list)


@app.route('/questions/2')
def question_2():
    return render_template('question_2.html', question_list=question_list)


@app.route('/questions/3')
def question_3():
    return render_template('question_3.html', question_list=question_list)


@app.route('/thanks')
def thank_you_page():
    return render_template('thanks.html')


@app.route('/answer')
def collect_answer():
    answer_0 = request.form['options']
    responses.add(answer_0)
    return render_template('answer.html', responses=responses)
