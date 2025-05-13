import os
from flask import Flask, request, redirect, url_for, flash, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
import ollama
import re

app = Flask(__name__)

# Use environment variables for sensitive data
app.secret_key = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI') or 'mysql://your_mysql_user:your_mysql_password@localhost/flask_auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100), unique=True, nullable=False)

class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    grade = db.Column(db.String(1), nullable=False)

def prepopulate_subjects():
    subjects = ['VLSI', 'Computer Networks', 'DSA', 'Software Engineering', 'Communication Engineering', 'Operating System']
    for subject_name in subjects:
        if not Subject.query.filter_by(subject_name=subject_name).first():
            new_subject = Subject(subject_name=subject_name)
            db.session.add(new_subject)
    db.session.commit()

def assign_random_grades(user_id):
    subjects = Subject.query.all()
    grades = ['A', 'B', 'C', 'D', 'F']
    for subject in subjects:
        random_grade = random.choice(grades)
        new_grade = Grade(user_id=user_id, subject_id=subject.id, grade=random_grade)
        db.session.add(new_grade)
    db.session.commit()

with app.app_context():
    db.create_all()
    prepopulate_subjects()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))  # ✅ Fixed for SQLAlchemy 2.0+

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')

        if not username or not email or not password or not full_name:
            flash('All fields are required.', 'danger')
            return redirect(url_for('signup'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists! Choose another one.', 'danger')
            return redirect(url_for('signup'))
        if User.query.filter_by(email=email).first():
            flash('Email already exists! Choose another one.', 'danger')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password, full_name=full_name)
        db.session.add(new_user)
        db.session.commit()

        assign_random_grades(new_user.id)

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        if not new_password:
            flash('New password is required.', 'danger')
            return redirect(url_for('reset_password'))

        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        current_user.password = hashed_password
        db.session.commit()
        flash('Password updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('reset_password.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
