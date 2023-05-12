from flask import Flask, render_template, request, url_for, redirect
import data_handler, util
import os

app = Flask(__name__)

@app.route('/')
def render_main_page():
    return render_template("index.html",
                           title="Home")


@app.route('/question')
def list_question():
    order_by_options = {'submission_time': 'Submission time', 'view_number': 'View number', 'vote_number': 'Vote number', 'title': 'Title'}
    order_options = ['DESC', 'ASC']
    order_by = request.args.get('order_by')
    order = request.args.get('order')
    questions = util.order_questions(order_by, order)
    return render_template("question.html",
                           data=questions,
                           title="List questions",
                           select_options=order_by_options,
                           order_options=order_options,
                           order_by=order_by,
                           order=order)

@app.route('/add-question', methods=["GET"])
def route_question():

    return render_template("add_question.html",
                           title="Add question")

@app.route('/add_question', methods=["POST"])
def add_question():
    new_question = {"view_number": 0,
                    "vote_number": 0,
                    "title": request.form.get("title"),
                    "message": request.form.get("message"),
                    "image": None}
    data_handler.add_question(new_question)

    return redirect(url_for("add_question"))

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    if request.method == 'POST':
        filter = request.form['filter']

        filtered = data_handler.filter_answer(filter=filter)

        return render_template('answer.html', answer=filtered)
    else:
        return render_template('filter_answer.html')
    
@app.route('/edit_answer', methods=['GET', 'POST'])
def edit_answer():

    data = data_handler.get_answer(id="1")

    if request.method == 'POST':
        edit_answer = request.form['edit_answer']

        edit = data_handler.edit_answer(edit_answer=edit_answer)
        return render_template('answer.html', answer=edit_answer)
    else:
        return render_template('edit_answer.html', data=data)


@app.route('/answer')
def answer_list():
    answer = data_handler.get_all_answer()
    return render_template('answer.html', answer=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0",
        port=8000,
        debug=True
            )
