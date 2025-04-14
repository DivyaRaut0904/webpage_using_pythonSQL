from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records")
    records = cursor.fetchall()
    conn.close()
    return render_template('index.html', records=records)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO records (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cursor.execute("UPDATE records SET name=?, email=? WHERE id=?", (name, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    cursor.execute("SELECT * FROM records WHERE id=?", (id,))
    record = cursor.fetchone()
    conn.close()
    return render_template('edit.html', record=record)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    conn.execute("DELETE FROM records WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
