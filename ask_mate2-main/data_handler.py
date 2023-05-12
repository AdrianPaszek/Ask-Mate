import connect

@connect.connection_handler
def get_all_questions(cursor, order_by, order):
  cursor.execute(f'select * from question order by {order_by} {order}')
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
                        'vote_number':dict['vote_number'],
                        'title': dict['title'],
                        'message': dict['message'],
                        'image': dict['image']})

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
def get_answer(cursor, id):
  cursor.execute("SELECT * FROM public.question WHERE ID = %s", (id))
  return cursor.fetchall()