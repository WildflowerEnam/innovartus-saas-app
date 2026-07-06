from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore, auth

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Initialize Firebase (you'll add your config)
# firebase_admin.initialize_app(cred)

# Mock user for demo (no Firebase required)
users = {
    'demo@innovartus.com': {'password': 'demo123', 'name': 'Demo User'}
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in users and users[email]['password'] == password:
            session['user_id'] = email
            session['user_name'] = users[email]['name']
            flash(f'Welcome back, {users[email]["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in users:
            flash('Email already registered', 'danger')
        else:
            users[email] = {'password': password, 'name': email.split('@')[0]}
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user_name=session.get('user_name'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)