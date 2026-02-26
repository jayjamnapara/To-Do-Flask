from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from app.models.models import User
from app import db
import re

auth_bp = Blueprint('auth', __name__)


def _is_valid_email(email: str) -> bool:
    return bool(re.match(r"^\S+@\S+\.\S+$", email))


@auth_bp.route("/register", methods=["POST", "GET"])
def Register():
    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")

        # Basic validations
        if not (fullname and email and phone and password):
            flash("All fields are required.", "danger")
            return render_template("Register.html", form_data=request.form)

        if not _is_valid_email(email):
            flash("Please enter a valid email address.", "danger")
            return render_template("Register.html", form_data=request.form)

        if not phone.isdigit() or len(phone) < 7 or len(phone) > 15:
            flash("Please enter a valid phone number (7-15 digits).", "danger")
            return render_template("Register.html", form_data=request.form)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("Register.html", form_data=request.form)

        # Check duplicate email
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("An account with this email already exists.", "danger")
            return render_template("Register.html", form_data=request.form)

        # Create user (note: passwords stored in plain-text here to match existing project)
        user = User(fullname=fullname, email=email, phone=phone, password=password)
        db.session.add(user)
        db.session.commit()
        flash("User registered successfully. Please log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template("Register.html", form_data={})
    
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not (email and password):
            flash('Email and password are required.', 'danger')
            return render_template('login.html', form_data=request.form)

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            flash("Logged in successfully", "success")
            return redirect(url_for('task.view_task'))

        flash("Invalid credentials. Please register or try again.", "danger")
        return render_template('login.html', form_data=request.form)

    return render_template('login.html', form_data={})

@auth_bp.route("/logout")
def logout():
    # session.pop('user_id', None)
    session.clear()
    flash('Logout Successfully!', "info")
    return redirect(url_for('auth.login'))

        