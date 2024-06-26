from flask import Flask, request, render_template, send_file
import os
from datetime import datetime, timedelta
from ics import Calendar, Event

app = Flask(__name__)

calendar = Calendar()
event_count = {}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add_event', methods=['POST'])
def add_event():
    day = request.form['day']
    time = request.form['time']
    name = request.form['name']
    duration = request.form['duration']
    notes = request.form['notes']
    all_day = request.form['all_day']
    
    duration = int(duration)
    start_date = get_next_day_date(day)
    
    add_event_to_ics(name, f"{start_date} {time}:00", duration, notes, all_day)
    return "Event added successfully!"

@app.route('/save_to_file', methods=['POST'])
def save_to_file():
    date_str = datetime.today().strftime('%Y-%m-%d')
    if date_str not in event_count:
        event_count[date_str] = 0
    event_count[date_str] += 1
    filename = f"{date_str}_event_{event_count[date_str]}.ics"
    folder_path = "ics_files"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as f:
        f.writelines(calendar)
    return send_file(file_path, as_attachment=True, download_name=filename)

def get_next_day_date(day_name):
    today = datetime.today()
    days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_name = day_name.lower()
    if day_name not in days_of_week:
        raise ValueError("Invalid day of the week.")
    today_weekday = today.weekday()
    target_weekday = days_of_week.index(day_name)
    days_ahead = (target_weekday - today_weekday + 7) % 7
    if days_ahead == 0:
        days_ahead = 7
    next_day_date = today + timedelta(days=days_ahead)
    return next_day_date.strftime('%Y-%m-%d')

def add_event_to_ics(event_name, start_time_str, duration_hours, notes, all_day):
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    if all_day == 'yes':
        end_time = start_time + timedelta(days=1)
    else:
        end_time = start_time + timedelta(hours=duration_hours)

    event = Event()
    event.name = event_name
    event.begin = start_time
    event.end = end_time
    event.description = notes
    event.transparent = (all_day == 'yes')

    calendar.events.add(event)

if __name__ == '__main__':
    app.run(debug=True)
