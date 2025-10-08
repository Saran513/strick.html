from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey' 
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

def get_db():
    conn = sqlite3.connect('contact.db')
    return conn

@app.route('/')
def home():
    return render_template('C:\\Users\\user\\Untitled-1.html')

@app.route('/about')
def about():
        return render_template('C:\\Users\\user\\Untitled-1.html')

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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
        if request.method == 'POST':
            password = request.form['password']
            if password == 'sv262002':  
                session['admin'] = True
                return redirect('/dashboard')
            else:
                return render_template('admin.html', error='Incorrect password')
        return render_template('admin.html', error=None)

@app.route('/dashboard')
def dashboard():
        if not session.get('admin'):
            return redirect('/admin')
        
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM contacts")
        messages = c.fetchall()
        conn.close()

        return render_template('dashboard.html', messages=messages)

if __name__ == '__main__':
        init_db()
        app.run(debug=True)
