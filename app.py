from flask import Flask, request, render_template, redirect, flash, jsonify, session
from surveys import satisfaction_survey as survey
from flask_debugtoolbar import DebugToolbarExtension

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def survey_start():
    """select a survey"""


    return render_template("survey_start.html", survey=survey)

   
@app.route("/start", methods=["POST"])
def survey_todo():
    
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

   
@app.route("/answer", methods=["POST"])
def answers():
    
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def show_question(qid):
    
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")
    if(len(responses) == len(survey.questions)):
        return redirect("/done")
    if(len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    question = survey.questions[qid]
    return render_template("question.html", q_num=qid, question=question, survey=survey)

 
@app.route("/done")
def finished():
    return render_template("done.html", survey=survey)