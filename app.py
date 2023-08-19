from flask import Flask, render_template, request, flash, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)
responses = []


@app.route("/")
def home():
    return render_template(
        "index.html", surveys=surveys["satisfaction"], responses=responses
    )


@app.route("/reset")
def reset():
    global responses
    responses = []
    return redirect("/")


@app.route("/questions/<int:q>", methods=["GET"])
def questions(q):
    if len(surveys["satisfaction"].questions) == len(responses):
        return redirect("/thankyou")
    if q != len(responses):
        flash("Denied invalid question sequences", "error")
        return redirect(f"/questions/{len(responses)}")
    question = surveys["satisfaction"].questions[q].question
    choices = surveys["satisfaction"].questions[q].choices
    return render_template("question.html", question=question, choices=choices)


@app.route("/answer", methods=["GET", "POST"])
def answer():
    global responses
    if not request.args:
        flash("Please Select one Answer", "error")
        return redirect(f"/questions/{len(responses)}")
    if len(surveys["satisfaction"].questions) == len(responses):
        return redirect("/")
    if request.method == "POST":
        print("HELLO")
    responses += list(request.args)

    return redirect(f"/questions/{len(responses)}")


@app.route("/thankyou")
def thanks():
    return render_template("thankyou.html")


if __name__ == "__main__":
    app.run(debug=True)
