from flask import Blueprint, flash, render_template, request, redirect, url_for
from app import db
from app.models import Event
from flask_login import current_user, login_required
from datetime import datetime

# Blueprint setup
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    # Fetch all events from the database
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', events=events)

@main_bp.route('/event/new', methods=['GET', 'POST'])
def create_event():
    if not current_user.is_authenticated:
        flash('You need to log in to create an event.', 'warning')
        return redirect(url_for('auth.login'))


    if request.method == 'POST':
        # Collect form data
        title = request.form['title']
        description = request.form.get('description')
        start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M').date()
        end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M').date()
        is_recurring = 'is_recurring' in request.form
        reminder_time = datetime.strptime(request.form['reminder_time'], '%Y-%m-%dT%H:%M') if request.form.get('reminder_time') else None
        recurrence = request.form.get('recurrence')
        
        # Create new event instance
        new_event = Event(
            user_id=current_user.id,  # Replace with a valid user ID from the `users` table
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            is_recurring=is_recurring,
            recurrence=recurrence,
            reminder_time=reminder_time
        )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('event.html')
