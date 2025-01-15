from . import db
from datetime import datetime
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.name}>"
    

# Add user_loader function in your app initialization
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Ensure nullable=False if user_id is required
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    is_recurring = db.Column(db.Boolean, default=False, nullable=False)
    recurrence = db.Column(db.String(50), nullable=True)
    reminder_time = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    created_at = db.Column(db.Date, default=datetime.utcnow)
    updated_at = db.Column(db.Date, default=datetime.utcnow, onupdate=datetime.utcnow)


    user = db.relationship('User', backref='events')

    def __repr__(self):
        return f"<Event {self.title}>"
