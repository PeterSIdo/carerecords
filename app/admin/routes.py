# VC:\Users\Peter\Documents\Care-Home-4\app\admin\routes.py
from flask import render_template, request, redirect, url_for, flash, session
from app.admin import bp  # Ensure this import is correct
import sqlite3
from datetime import datetime
from app.login_check import login_required

@bp.route('/admin_dashboard')
@login_required(user_mode='a')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@bp.route('/enter_resident', methods=['GET', 'POST'])
def enter_resident():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        if request.method == 'POST':
            resident_name = request.form.get('resident_name')
            resident_surname = request.form.get('resident_surname')
            unit_name = request.form.get('unit_name')
            room_nr = request.form.get('room_nr')

            # Convert room_nr to an integer
            try:
                room_nr = int(room_nr)
            except ValueError:
                flash('Room number must be an integer.')
                return redirect(url_for('admin.enter_resident'))
            
            # Calculate resident initials
            initials = resident_name[0].upper() + resident_surname[0].upper()
            resident_initials = f"{unit_name}{room_nr:02d}{initials}"
            
            # Connect to the database
            conn = sqlite3.connect('care4.db')
            cursor = conn.cursor()

            # Check for duplicates
            cursor.execute('SELECT id FROM residents WHERE unit_name = ? AND room_nr = ?', (unit_name, room_nr))
            existing_resident = cursor.fetchone()

            if existing_resident:
                # Duplicate found, prompt for confirmation
                if request.form.get('confirm') == 'Sure':
                    # User confirmed, overwrite the existing record
                    cursor.execute('UPDATE residents SET resident_name = ?, resident_surname = ?, resident_initials = ? WHERE id = ?', 
                                   (resident_name, resident_surname, resident_initials, existing_resident[0]))
                    flash('Resident record updated successfully!')
                else:
                    # Prompt user for confirmation
                    flash('Are you sure you want to overwrite?', 'warning')
                    return render_template('enter_resident.html', confirm=True, resident_name=resident_name, resident_surname=resident_surname, unit_name=unit_name, room_nr=room_nr)
            else:
                # No duplicate, insert new record
                cursor.execute('INSERT INTO residents (resident_name, resident_surname, unit_name, room_nr, resident_initials) VALUES (?, ?, ?, ?, ?)', 
                               (resident_name, resident_surname, unit_name, room_nr, resident_initials))
                flash('Resident added successfully!')

            # Commit changes and close connection
            conn.commit()
            conn.close()

            return redirect(url_for('admin.enter_resident'))

        return render_template('enter_resident.html')
    return redirect(url_for('login.login'))


@bp.route('/list_all_residents')
@login_required(user_mode='a')
def list_all_residents():
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT resident_initials, resident_name, resident_surname, unit_name, room_nr FROM residents')
    residents = cursor.fetchall()
    conn.close()
    return render_template('list_all_residents.html', residents=residents)

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
        return redirect(url_for('admin.residents_observations_input'))

    # Fetch unit names from the database
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT unit_name FROM units')
    units = cursor.fetchall()
    
    cursor.execute('SELECT DISTINCT observation_name FROM residents_observations_list')
    observations = cursor.fetchall()
    conn.close()

    return render_template('residents_observations_input.html', units=units, observations=observations)