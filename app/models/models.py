from app import db
from datetime import datetime

date_obj = datetime.now()
date_str = datetime.strftime(date_obj,"%Y-%b-%d %H:%M:%S")
print(date_str)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String, nullable = False)
    email = db.Column(db.String, unique = True)
    phone = db.Column(db.String, nullable = False)
    password= db.Column(db.String, nullable = False)
    tasks = db.relationship("Tasks", backref = 'user') 

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.strptime(date_str, "%Y-%b-%d %H:%M:%S"))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
