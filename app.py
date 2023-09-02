from flask import Flask, render_template, request, flash, redirect, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def home():
    return render_template(
        "index.html",
        surveys=surveys["satisfaction"],
        responses=session.get("responses", []),
    )


@app.route("/start-survey")
def start_survey():
    session["responses"] = []
    return redirect("questions/0")


@app.route("/reset")
def reset():
    session["responses"] = []
    return redirect("/")


@app.route("/questions/<int:q>", methods=["GET"])
def questions(q):
    print(f' LENGTH: {len(list(session["responses"]))} == ={session["responses"]}')
    if len(surveys["satisfaction"].questions) == len(session["responses"]):
        return redirect("/thankyou")
    if q != len(session["responses"]):
        flash("Denied invalid question sequences", "error")
        return redirect(f"/questions/{len(session['responses'])}")
    question = surveys["satisfaction"].questions[q].question
    choices = surveys["satisfaction"].questions[q].choices
    return render_template("question.html", question=question, choices=choices)


@app.route("/answer", methods=["GET", "POST"])
def answer():
    if not request.args:
        flash("Please Select one Answer", "error")
        return redirect(f"/questions/{len(session['responses'])}")
    if len(surveys["satisfaction"].questions) == len(session["responses"]):
        return redirect("/")
    session["responses"] += list(request.args)

    return redirect(f"/questions/{len(session['responses'])}")


@app.route("/thankyou")
def thanks():
    return render_template("thankyou.html")


if __name__ == "__main__":
    app.run(debug=True)
