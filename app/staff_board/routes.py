# c:/Users/Peter/Documents/Care-Home-4/app/staff_board/routes.py
from flask import render_template, request, redirect, url_for, flash
from app.staff_board import bp
import sqlite3
from datetime import datetime

@bp.route('/staff_dashboard')
def staff_dashboard():
    return render_template('staff_dashboard.html')

@bp.route('/residents_observations_input', methods=['GET', 'POST'])
def residents_observations_input():
    if request.method == 'POST':
        # Collect form data
        resident_initials = request.form.get('resident_initials')
        unit_name = request.form.get('unit_name')
        observation_name = request.form.get('observation_name')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        observation_reason = request.form.get('observation_reason')
        observation_notes = request.form.get('observation_notes')   
        staff_initials = request.form.get('staff_initials')
        
        # Validate form data
        if not (resident_initials and unit_name):
            flash('Please fill out all required fields.')
            return redirect(url_for('staff_board.residents_observations_input'))

        # Insert data into the database
        conn = sqlite3.connect('care4.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO residents_observations_chart (
                resident_initials, unit_name, observation_name, start_date, end_date, observation_reason, observation_notes, staff_initials
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (resident_initials, unit_name, observation_name, start_date, end_date, observation_reason, observation_notes, staff_initials))
        conn.commit()
        conn.close()

        flash('Observation recorded successfully!', 'success')
        return redirect(url_for('staff_board.residents_observations_input'))

    # Fetch unit names from the database
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT unit_name FROM units')
    units = cursor.fetchall()
    
    cursor.execute('SELECT DISTINCT observation_name FROM residents_observations_list')
    observations = cursor.fetchall()
    conn.close()

    return render_template('residents_observations_input.html', units=units, observations=observations)

# c:/Users/Peter/Documents/Care-Home-4/app/staff_board/routes.py
@bp.route('/residents_observations_chart')
def residents_observations_chart():
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    
    # Fetch only non-expired records
    cursor.execute('''
        SELECT * FROM residents_observations_chart
        WHERE end_date > ?
    ''', (datetime.now().strftime('%Y-%m-%dT%H:%M'),))
    
    observations = cursor.fetchall()
    conn.close()

    # Format the start_date and end_date
    formatted_observations = []
    for observation in observations:
        observation = list(observation)
        observation[4] = datetime.strptime(observation[4], '%Y-%m-%dT%H:%M').strftime('%d-%m-%y %H:%M')
        observation[5] = datetime.strptime(observation[5], '%Y-%m-%dT%H:%M').strftime('%d-%m-%y %H:%M')
        formatted_observations.append(observation)

    return render_template('residents_observations_chart.html', observations=formatted_observations)