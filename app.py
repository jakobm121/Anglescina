from flask import Flask, render_template, request, session, redirect, url_for
import json
import random
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as file:
        return json.load(file)


def init_progress():
    if "score" not in session:
        session["score"] = {"correct": 0, "wrong": 0}


def add_result(is_correct):
    init_progress()
    score = session["score"]
    if is_correct:
        score["correct"] += 1
    else:
        score["wrong"] += 1
    session["score"] = score


@app.route("/")
def home():
    init_progress()
    return render_template("index.html", score=session["score"])


@app.route("/vocabulary", methods=["GET", "POST"])
def vocabulary():
    words = load_json("vocabulary.json")
    result = None
    previous_word = None

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip().lower()
        correct_answer = request.form.get("correct_answer", "").strip().lower()
        previous_word = request.form.get("slovenian", "")
        is_correct = user_answer == correct_answer
        add_result(is_correct)
        if is_correct:
            result = {"type": "success", "text": "Pravilno!"}
        else:
            result = {"type": "error", "text": f"Ni pravilno. Pravilen odgovor je: {correct_answer}"}

    word = random.choice(words)
    return render_template("vocabulary.html", word=word, result=result, previous_word=previous_word)


@app.route("/grammar", methods=["GET", "POST"])
def grammar():
    exercises = load_json("grammar.json")
    result = None

    if request.method == "POST":
        user_answer = request.form.get("answer", "")
        correct_answer = request.form.get("correct_answer", "")
        explanation = request.form.get("explanation", "")
        is_correct = user_answer == correct_answer
        add_result(is_correct)
        if is_correct:
            result = {"type": "success", "text": "Pravilno!", "explanation": explanation}
        else:
            result = {"type": "error", "text": f"Ni pravilno. Pravilen odgovor je: {correct_answer}", "explanation": explanation}

    exercise = random.choice(exercises)
    return render_template("grammar.html", exercise=exercise, result=result)


@app.route("/writing", methods=["GET", "POST"])
def writing():
    feedback = None
    text = ""
    prompts = load_json("writing_prompts.json")
    prompt = random.choice(prompts)

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        word_count = len(text.split())
        if word_count < 8:
            feedback = {"type": "error", "text": "Poskusi napisati malo daljši odgovor, vsaj 8 besed."}
        else:
            feedback = {"type": "success", "text": f"Dobro! Napisal/a si približno {word_count} besed. Preberi še enkrat in preveri velike začetnice, pike in čas glagolov."}
            add_result(True)

    return render_template("writing.html", prompt=prompt, feedback=feedback, text=text)


@app.route("/progress")
def progress():
    init_progress()
    score = session["score"]
    total = score["correct"] + score["wrong"]
    percent = round((score["correct"] / total) * 100, 1) if total else 0
    return render_template("progress.html", score=score, total=total, percent=percent)


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
