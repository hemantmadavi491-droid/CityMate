from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import requests

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'citymate_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///citymate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================
# DATABASE MODELS
# ==========================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    complaint_id = db.Column(db.String(20), unique=True)

    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    status = db.Column(db.String(50), default='Pending')

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))
    message = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

# ==========================
# HOME
# ==========================

@app.route('/')
def home():

    announcements = Announcement.query.order_by(
        Announcement.created_at.desc()
    ).limit(3).all()

    return render_template(
        'index.html',
        announcements=announcements
    )

# ==========================
# REGISTER
# ==========================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(
            request.form['password']
        )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))

        user = User(
            name=name,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        flash('Registration Successful!', 'success')

        return redirect(url_for('login'))

    return render_template('register.html')

# ==========================
# LOGIN
# ==========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session['user_id'] = user.id
            session['user_name'] = user.name

            flash('Login Successful!', 'success')

            return redirect(url_for('home'))

        flash('Invalid Credentials', 'danger')

    return render_template('login.html')

# ==========================
# LOGOUT
# ==========================

@app.route('/logout')
def logout():

    session.clear()

    flash('Logged Out Successfully', 'success')

    return redirect(url_for('home'))

# ==========================
# SERVICES
# ==========================

@app.route('/services')
def services():
    return render_template('services.html')

# ==========================
# FILE COMPLAINT
# ==========================

@app.route('/complaint', methods=['GET', 'POST'])
def complaint():

    if request.method == 'POST':

        complaint_number = (
            "CMP" +
            str(random.randint(10000, 99999))
        )

        new_complaint = Complaint(
            complaint_id=complaint_number,
            title=request.form['title'],
            category=request.form['category'],
            description=request.form['description']
        )

        db.session.add(new_complaint)
        db.session.commit()

        flash(
            f'Complaint Submitted Successfully! ID: {complaint_number}',
            'success'
        )

        return redirect(url_for('complaints'))

    return render_template('complaint.html')

# ==========================
# VIEW COMPLAINTS
# ==========================

@app.route('/complaints')
def complaints():

    complaints = Complaint.query.order_by(
        Complaint.created_at.desc()
    ).all()

    return render_template(
        'complaints.html',
        complaints=complaints
    )

# ==========================
# COMPLAINT DETAILS
# ==========================

@app.route('/complaint/<int:id>')
def complaint_detail(id):

    complaint = Complaint.query.get_or_404(id)

    return render_template(
        'complaint_detail.html',
        complaint=complaint
    )

# ==========================
# ANNOUNCEMENTS
# ==========================

@app.route('/announcements')
def announcements():

    announcements = Announcement.query.order_by(
        Announcement.created_at.desc()
    ).all()

    return render_template(
        'announcements.html',
        announcements=announcements
    )

# ==========================
# ADMIN DASHBOARD
# ==========================

@app.route('/admin')
def admin_dashboard():

    complaints = Complaint.query.order_by(
        Complaint.created_at.desc()
    ).all()

    total_users = User.query.count()
    total_complaints = Complaint.query.count()

    return render_template(
        'admin_dashboard.html',
        complaints=complaints,
        total_users=total_users,
        total_complaints=total_complaints
    )

# ==========================
# UPDATE COMPLAINT STATUS
# ==========================

@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):

    complaint = Complaint.query.get_or_404(id)

    complaint.status = request.form['status']

    db.session.commit()

    flash(
        'Complaint Status Updated!',
        'success'
    )

    return redirect(url_for('admin_dashboard'))

@app.route('/search_services', methods=['GET', 'POST'])
def search_services():

    results = []
    error = None

    if request.method == 'POST':

        city = request.form['city']
        category = request.form['category']

        query = f"{category} in {city}"

        url = (
            "https://nominatim.openstreetmap.org/search"
            f"?q={query}"
            "&format=json"
            "&limit=20"
        )

        headers = {
            "User-Agent": "CityMate"
        }

        try:

            response = requests.get(
                url,
                headers=headers
            )

            results = response.json()

        except Exception as e:

            error = str(e)

    return render_template(
        'search_services.html',
        results=results,
        error=error
    )

# ==========================
# CREATE DATABASE
# ==========================

with app.app_context():
    db.create_all()

# ==========================
# RUN APP
# ==========================

if __name__ == '__main__':
    app.run(debug=True)