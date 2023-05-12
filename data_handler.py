import connect

@connect.connection_handler
def get_all_questions(cursor, order_by, order):
  cursor.execute(f'select * from question order by {order_by} {order}')
  question = cursor.fetchall()
  return question

@connect.connection_handler
def show_question(cursor, question_id):
    cursor.execute(f"""select * from question where id = {question_id}""")
    question = cursor.fetchall()
    return question

@connect.connection_handler
def add_question(cursor, dict):
    from datetime import datetime
    dt = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
                        INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
                        VALUES(%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);
                         """,
                       {'submission_time': dt,
                        'view_number': dict['view_number'],
                        'vote_number': dict['vote_number'],
                        'title': dict['title'],
                        'message': dict['message'],
                        'image': dict['image']})

@connect.connection_handler
def add_answer(cursor, dict):
    from datetime import datetime
    dt = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
                        INSERT INTO answer(submission_time, vote_number, question_id, message, image)
                        VALUES(%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s);
                        """,
                       {'submission_time': dt,
                        'vote_number': dict['vote_number'],
                        'question_id': dict['question_id'],
                        'message': dict['message'],
                        'image': dict['image']})

@connect.connection_handler
def get_searched_questions(cursor, search_phrase):
    cursor.execute("SELECT * FROM question WHERE title LIKE %s OR message LIKE %s", ('%'+search_phrase+'%', '%'+search_phrase+'%'))
    return cursor.fetchall()

@connect.connection_handler
def get_all_answer(cursor):
  query = "SELECT * FROM public.answer"
  cursor.execute(query)
  return cursor.fetchall()

@connect.connection_handler
def filter_answer(cursor, filter):
  cursor.execute("SELECT * FROM public.question WHERE LOWER(message) LIKE LOWER(%s)", ('%' + filter + '%',))
  return cursor.fetchall()

@connect.connection_handler
def update_answer(cursor, message, title, id):
  cursor.execute("UPDATE public.question SET message = '%s', title = '%s' WHERE id = '%s'", (message, title, id))
  return cursor.fetchall()
# UPDATE public.question SET message = 'This is the updated message.' WHERE id = 1;
# SELECT * FROM public.question WHERE ID = 1

@connect.connection_handler
def get_answer(cursor,id):
  cursor.execute(f"""SELECT message FROM answer where question_id = {id}""")
  return cursor.fetchall()

@connect.connection_handler
def latest_questions(cursor):
    cursor.execute("SELECT * FROM question ORDER BY submission_time DESC LIMIT 5")
    return cursor.fetchall()

@connect.connection_handler
def show_question_comments(cursor, question_id):
    cursor.execute(f"""
                    SELECT * FROM comment
                    WHERE question_id = {question_id};
                    """)
    comments = cursor.fetchall()
    return comments

@connect.connection_handler
def add_answer_comment(cursor, dict):
    from datetime import datetime
    dt = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(""" 
                    INSERT INTO comment(question_id, answer_id, message, submission_time, edited_count)
                        VALUES(%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s);
                        """,
                       {'question_id': dict['question_id'],
                        'answer_id': dict['answer_id'],
                        'message': dict['message'],
                        'submission_time': dt,
                        'edited_count': dict['edited_count']})
    comments = cursor.fetchall()
    return comments
    
@connect.connection_handler
def get_question_vote_number(cursor, question_id):
   cursor.execute(f"""SELECT vote_number FROM question WHERE ID = {question_id}""")
   question = cursor.fetchall()
   return question[0]['vote_number']

@connect.connection_handler
def show_answer_comments(cursor, answer_id):
    cursor.execute(f"""
                    SELECT * FROM comment
                    WHERE answer_id = {answer_id};
                    """)
    
@connect.connection_handler
def vote_plus(cursor, question_id):
    cursor.execute(f"""UPDATE question SET vote_number = vote_number + 1
                    WHERE id = {question_id}""")
    
@connect.connection_handler
def vote_minus(cursor, question_id):
    cursor.execute(f"""UPDATE question SET vote_number = vote_number - 1
                    WHERE id = {question_id}""")
