from flask import Flask, render_template, request, url_for, redirect
import data_handler, util
import os

app = Flask(__name__)

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
@app.route('/')
def render_main_page():
    questions = data_handler.latest_questions()
    items = [{'id': question['id'], 'title': question['title'], 'submission_time': question['submission_time'], 'message': question['message']} for question in questions]
    return render_template("index.html", title="Home", latest_questions=items)

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

    return redirect(url_for("render_main_page")) #u sophii jest przekierowanie na list_question


@app.route('/question/<int:question_id>', methods=["GET", "POST"])
def show_question(question_id):
    question = data_handler.show_question(question_id)
    answers = data_handler.get_answer(question_id)
    comments = data_handler.show_answer_comments(question_id)
    vote_type = request.form.get('vote_type',)
    if request.method == 'POST':
        if vote_type == 'like':
            data_handler.vote_plus(question_id)
        elif vote_type == 'dislike':
            data_handler.vote_minus(question_id)
        return redirect(url_for('show_question', question_id=question_id))
    vote_number = data_handler.get_question_vote_number(question_id)
    return render_template('show_question.html',
                           question=question,
                           answers=answers,
                           comments=comments,
                           vote_number=vote_number,
                           )

@app.route('/question/<question_id>/new-answer', methods=["GET", "POST"])
def route_new_answer(question_id):
    if request.method == "POST":
        new_answer = {'vote_number': 0,
                  'question_id': question_id,
                  'message': request.form.get('message'),
                  'image': None}
        print(new_answer)
        if new_answer['message'] != None:
            data_handler.add_answer(new_answer)
        return render_template("new-answer.html",
                        question_id=question_id,
                        title="new answer")
    return redirect(url_for('new-answer', question_id=question_id))

@app.route('/answer/<answer_id>/new_comment', methods=["GET"])
def route_new_answer_comment(answer_id):
    question_id = request.args.get("question_id")
    return render_template('add_answer_comment.html',
                           answer_id=answer_id,
                           question_id=question_id,
                           title='New comment')

@app.route('/question/<int:question_id>/vote')
def vote_for_question(question_id):
    vote_type = request.form.get('vote_type')
    title = request.args.get('title')
    vote_number = data_handler.get_question_vote_number(question_id)
    increases_or_decreases_vote_number = util.vote_up_or_down(vote_number, vote_type)
    data_handler.update_question_vote_number(question_id, increases_or_decreases_vote_number)
    if title == 'Main page':
        return redirect(url_for("get_last_5_questions_by_time"))
    # return redirect(i gidześ tam"))


                    
@app.route('/answer/<int:answer_id>/new_comment', methods=["POST"])
def add_answer_comment(answer_id):
    question_id = request.args.get("question_id")
    new_comment = {
                    'question_id': None,
                    'answer_id': answer_id,
                    'message': request.form.get("message"),
                    'edited_count': 0
                    }
    data_handler.add_answer_comment(new_comment)

    return redirect(url_for("show_answer",
                            answer_id=answer_id,
                            question_id=question_id))

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
    print(answer)
    return render_template('answer.html', answer=answer)

@app.route('/found_questions', methods = ['POST', 'GET'])
def found_questions():
    search_phrase = request.form.get('search')
    x = data_handler.get_searched_questions(search_phrase)
    return render_template('found_questions.html', x = x)

if __name__ == "__main__":
    app.run(host="0.0.0.0",
        port=8000,
        debug=True
            )
