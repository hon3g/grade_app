import sqlite3
from flask import Flask, request, session, g, redirect, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'


def connect_db():
    db = sqlite3.connect("hw13.db")
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_db(Exception):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.before_request
def before_request():
    g.db = connect_db()

@app.route('/')
def index():
    redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            return redirect('/dashboard')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session['username'] == 'admin':
        cur = g.db.execute("SELECT * FROM student")
        cur2 = g.db.execute("SELECT * FROM quiz")

        res = cur.fetchall()
        res2 = cur2.fetall()

        students = [dict(s_id=r[0], f_name=r[1], l_name=r[2]) for r in res]
        quizzes = [dict(q_id=r[0], sub=r[1], num_que=r[2], date=r[3]) for r in res2]

        return render_template('dashboard.html', students=students, quizzes=quizzes)
    else:
        return redirect('/login')

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if session['username'] == 'admin':
        if request.method == 'GET':
            return render_template('add_student.html')
        elif request.method == 'POST':
            try:
                g.db.execute("INSERT INTO student (first_name, last_name) VALUES (?, ?)",
                             [request.form['first_name'], request.form['last_name']])
                g.db.commit()
                return redirect('/dashboard')
            except Exception as e:
                print(e)
                return render_template('add_student.html')
    else:
        redirect('/login')

@app.route('/student/<id>')
def get_results(id):
    cur = g.db.execute("""SELECT quiz.quiz_id, quiz_result.score, quiz.date_given, quiz.subject
                          FROM student
                          JOIN quiz_result ON student.student_id = quiz_result.student_id
                          JOIN quiz ON quiz_result.quiz_id = quiz.quiz_id
                          WHERE student.student_id = ?""", [id])
    res = cur.fetchall()
    results = [dict(q_id=r[0], score=r[1], q_date=r[2], q_subject=r[3]) for r in res]

    return render_template('student_result.html', results=results)


if __name__ == '__main__':
    con = sqlite3.connect("hw13.db")
    con.cursor().executescript(open("schema.sql").read())

    app.run(debug=True)
