from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Event

# Blueprint setup
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Fetch all events from the database
    events = Event.query.all()
    return render_template('index.html', events=events)

@main_bp.route('/event/new', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        # Collect form data
        title = request.form['title']
        description = request.form.get('description')
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        is_recurring = 'is_recurring' in request.form
        
        # Create new event instance
        new_event = Event(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            is_recurring=is_recurring
        )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('event.html')
