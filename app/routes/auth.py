from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from app.models.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["POST", "GET"])
def Register():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

        if fullname and email and phone and password:
            user = User(fullname=fullname, email=email, phone=phone, password=password)
            db.session.add(user)
            db.session.commit()
            flash("User Register Successfully", "info")
        return redirect(url_for('auth.login'))
    return render_template("Register.html")    
    
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            email = request.form.get('email'),
            password = request.form.get('password')
        ).first()

        if user:
            session['user_id'] = user.id
            flash("logged In Successfully", "success")
            return redirect(url_for('task.view_task'))
        else:
            flash("Please Register First", "Info")
    return render_template('login.html')

@auth_bp.route("/logout")
def logout():
    # session.pop('user_id', None)
    session.clear()
    flash('Logout Successfully!', "info")
    return redirect(url_for('auth.login'))

        