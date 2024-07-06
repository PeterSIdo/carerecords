# app/reports/routes.py
from flask import render_template, request, url_for, redirect, session, flash
from app.reports import bp
import sqlite3
from datetime import datetime

@bp.route('/report_selection', methods=['GET', 'POST'])
def report_selection():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'c':
        if request.method == 'POST':
            unit_name = request.form.get('unit_name')
            resident_initials = request.form.get('resident_initials')
            service_name = request.form.get('service_name')
            
            if not unit_name or not resident_initials or not service_name:
                flash('Please enter unit name, resident initials, and select a service.')
                return redirect(url_for('reports.report_selection'))
            
            # Redirect to report_selection_logic blueprint with selected service
            return redirect(url_for('reports.report_selection_logic', unit_name=unit_name, resident_initials=resident_initials, service_name=service_name))
        
        # Fetch service list and unit list from the database
        conn = sqlite3.connect('care4.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, service_name FROM service_list')
        services = cursor.fetchall()
        cursor.execute('SELECT DISTINCT unit_name FROM units')  # Updated query
        units = cursor.fetchall()
        conn.close()
        
        return render_template('report_selection.html', services=services, units=units)
    return redirect(url_for('login.login'))

@bp.route('/report_selection_logic', methods=['GET', 'POST'])
def report_selection_logic():
    if request.method == 'POST':
        unit_name = request.form.get('unit_name')
        resident_initials = request.form.get('resident_initials')
        service_name = request.form.get('service_name')
    else:  # Handle GET request
        unit_name = request.args.get('unit_name')
        resident_initials = request.args.get('resident_initials')
        service_name = request.args.get('service_name')

    if service_name == 'fluid intake':
        return redirect(url_for('reports.report_fluid', unit_name=unit_name, resident_initials=resident_initials))
    elif service_name == 'food intake':
        return redirect(url_for('data_collection.food_intake', unit_name=unit_name, resident_initials=resident_initials))
    else:
        return redirect(url_for('login.login'))

# c:/Users/Peter/Documents/Care-Home-4/app/reports/routes.py

@bp.route('/report_fluid')
def report_fluid():
    resident_initials = request.args.get('resident_initials')
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM fluid_chart 
        WHERE resident_initials = ?
        ORDER BY timestamp ASC
    ''', (resident_initials,))
    data = cursor.fetchall()
    conn.close()

    # Convert timestamp strings to datetime objects
    formatted_data = []
    for row in data:
        row = list(row)
        row[2] = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')  # Format without seconds
        formatted_data.append(row)

    return render_template('report_fluid.html', data=formatted_data)