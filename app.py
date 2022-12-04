from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
"""turn the redicrect message off"""
debug = DebugToolbarExtension(app)


@app.route('/survey')
def surve_page():
    print(satisfaction_survey)
    return render_template('survey.html', responses=responses)


@app.route('/survey/result', methods=['POST'])
def show_result():
    answer = request.form['answer']
    responses.append(answer)
    return redirect('/survey')


responses = []
