from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from app.models.models import Tasks
from app import db
from datetime import datetime

task_bp = Blueprint('task', __name__)

@task_bp.route("/")
def view_task():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    tasks = Tasks.query.filter_by(user_id = user_id).all()
    return render_template("tasks.html", Tasks=tasks)

@task_bp.route("/add", methods=["GET", "POST"])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    title = request.form.get('title')
    due_date = request.form.get('due_date')
    user_id = session['user_id']
    # Validate inputs
    if not title or not title.strip():
        flash('Task title is required.', 'danger')
        return redirect(url_for('task.view_task'))

    if not due_date:
        flash('Due date is required.', 'danger')
        return redirect(url_for('task.view_task'))

    try:
        due_py_date = datetime.strptime(due_date, "%Y-%m-%d")
    except (ValueError, TypeError):
        flash('Invalid due date format. Use YYYY-MM-DD.', 'danger')
        return redirect(url_for('task.view_task'))

    task = Tasks(
        title=title.strip(),
        due_date=due_py_date,
        user_id=user_id
    )
    db.session.add(task)
    db.session.commit()
    flash('Task added successfully.', 'success')
    return redirect(url_for('task.view_task'))

@task_bp.route('/clear', methods=["POST"])
def clear():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    Tasks.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    flash('All your tasks were deleted successfully.', 'info')
    return redirect(url_for('task.view_task'))

@task_bp.route('/toggle/<int:task_id>', methods=["GET", "POST"])
def toggle_status(task_id):
    task = Tasks.query.get(task_id)
    if not task:
        flash('Task not found.', 'danger')
        return redirect(url_for('task.view_task'))

    # Normalize status toggling
    task.status = "Done" if (str(task.status).lower() == "pending") else "Pending"
    db.session.commit()
    return redirect(url_for("task.view_task"))

@task_bp.route('/delete/<int:task_id>', methods=["GET", "POST"])
def delete_task(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        flash(f"Task {task_id} is Deleted successfully!", "info")
    else:
        flash('Task Not Found!', 'danger')
    return redirect(url_for("task.view_task"))

@task_bp.route('/update/<int:task_id>', methods=["GET", "POST"])
def update_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # find the task 
    task = Tasks.query.filter_by(id=task_id).first()

    # check if not task find give error.
    if not task:
        flash('Task Not Found!', "danger")
        return redirect(url_for('task.view_task'))
    
    # if found the task get data from html.
    if request.method   == "POST":
        new_title = request.form.get('title')
        new_due_date = request.form.get('due_date')

        # update field only if are they provided into from.
        if new_title:
            task.title = new_title
        if new_due_date:
            # task.due_date = new_due_date
            try:
                parse_date = datetime.strptime(new_due_date, "%Y-%m-%d")
                task.due_date = parse_date
            except ValueError:
                flash('Invalid Date Format', 'warning')
                all_task = Tasks.query.filter_by(user_id=session['user_id']).all()
                return render_template("tasks.html", Tasks=all_task, edit_task=task)

        # after the update commit to save data into the Database.
        db.session.commit()
        flash('Task updated successfully', "success")
        return redirect(url_for('task.view_task'))
    
    # show the main page but highlight this task to editing.
    all_task = Tasks.query.filter_by(user_id = session['user_id']).all()
    return render_template("tasks.html", Tasks=all_task, edit_task=task)