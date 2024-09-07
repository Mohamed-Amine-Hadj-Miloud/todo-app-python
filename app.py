from flask import Flask, render_template, request, redirect,url_for
import sqlite3
app = Flask(__name__)
# Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
# Initialize the database
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            complete BOOLEAN NOT NULL DEFAULT 0
            Todo App flask3)
            ''')
    conn.commit()
    conn.close()
@app.route('/')
def index():
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return render_template('index.html', todos=todos)
@app.route('/add', methods=('POST',))
def add():
    task = request.form['task']
    if task:
        conn = get_db_connection()
        conn.execute('INSERT INTO todos (task) VALUES (?)',(task,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))
@app.route('/complete/<int:todo_id>')
def complete(todo_id):
    conn = get_db_connection()
    conn.execute('UPDATE todos SET complete = 1 WHERE id =?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
if __name__ == '__main__':
    init_db()
    app.run(debug=True)