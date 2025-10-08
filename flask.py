from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database init function
def init_db():
    conn = sqlite3.connect('contact.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# Simple DB connector
def get_db():
    return sqlite3.connect('contact.db')

@app.route('/')
def home():
    return render_template('login.html')  # show the login page first

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']

        # Basic hardcoded check
        if password == 'sv262002' and username == '9443042186':
            session['admin'] = True
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Incorrect credentials')
    return render_template('login.html', error=None)

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/')

    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    messages = c.fetchall()
    conn.close()

    return render_template('dashboard.html', messages=messages)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
              (name, email, message))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
