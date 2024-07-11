# c:/Users/Peter/Documents/Care-Home-4/app/reports/routes.py
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
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            
            if not unit_name or not resident_initials or not service_name or not start_date or not end_date:
                flash('Please enter all required fields.')
                return redirect(url_for('reports.report_selection'))
            
            if service_name == 'fluid intake':
                total_fluid_volume = fetch_and_summarize_fluid_volume(resident_initials, start_date, end_date)
                flash(f'Total Fluid Volume: {total_fluid_volume} ml')
            
            # Redirect to report_selection_logic blueprint with selected service and date range
            return redirect(url_for('reports.report_selection_logic', unit_name=unit_name, resident_initials=resident_initials, service_name=service_name, start_date=start_date, end_date=end_date))
        
        # Fetch service list and unit list from the database
        conn = sqlite3.connect('care4.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, service_name FROM service_list')
        services = cursor.fetchall()
        cursor.execute('SELECT DISTINCT unit_name FROM units')  # Updated query
        units = cursor.fetchall()
        conn.close()
        
        # Get current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        return render_template('report_selection.html', services=services, units=units, current_date=current_date)
    return redirect(url_for('login.login'))

@bp.route('/report_selection_logic', methods=['GET', 'POST'])
def report_selection_logic():
    if request.method == 'POST':
        unit_name = request.form.get('unit_name')
        resident_initials = request.form.get('resident_initials')
        service_name = request.form.get('service_name')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
    else:  # Handle GET request
        unit_name = request.args.get('unit_name')
        resident_initials = request.args.get('resident_initials')
        service_name = request.args.get('service_name')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

    if service_name == 'fluid intake':
        return redirect(url_for('reports.report_fluid', unit_name=unit_name, resident_initials=resident_initials, start_date=start_date, end_date=end_date))
    elif service_name == 'food intake':
        return redirect(url_for('reports.report_food', unit_name=unit_name, resident_initials=resident_initials, start_date=start_date, end_date=end_date))
    elif service_name == 'personal care':
        return redirect(url_for('reports.report_personal_care', unit_name=unit_name, resident_initials=resident_initials, start_date=start_date, end_date=end_date))
    elif service_name == 'cardex':
        return redirect(url_for('reports.report_cardex', unit_name=unit_name, resident_initials=resident_initials, start_date=start_date, end_date=end_date))
    else:
        return redirect(url_for('login.login'))

@bp.route('/report_fluid')
def report_fluid():
    resident_initials = request.args.get('resident_initials')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT resident_initials, timestamp, fluid_type, fluid_volume, fluid_note, staff_initials 
        FROM fluid_chart 
        WHERE resident_initials = ? AND timestamp BETWEEN ? AND ?
        ORDER BY timestamp ASC
    ''', (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    data = cursor.fetchall()
    conn.close()

    # Convert timestamp strings to datetime objects
    formatted_data = []
    for row in data:
        row = list(row)
        row[1] = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')  # Format without seconds
        formatted_data.append(row)

    return render_template('report_fluid.html', data=formatted_data)

def fetch_and_summarize_fluid_volume(resident_initials, start_date, end_date):
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT fluid_volume FROM fluid_chart 
        WHERE resident_initials = ? AND timestamp BETWEEN ? AND ?
    ''', (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    data = cursor.fetchall()
    conn.close()
    
    total_fluid_volume = sum(row[0] for row in data)
    return total_fluid_volume

@bp.route('/report_food')
def report_food():
    resident_initials = request.args.get('resident_initials')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT resident_initials, timestamp, food_type, food_amount, food_note, staff_initials 
        FROM food_chart 
        WHERE resident_initials = ? AND timestamp BETWEEN ? AND ?
        ORDER BY timestamp ASC
    ''', (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    data = cursor.fetchall()
    conn.close()

    # Convert timestamp strings to datetime objects
    formatted_data = []
    for row in data:
        row = list(row)
        row[1] = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')  # Format without seconds
        formatted_data.append(row)

    return render_template('report_food.html', data=formatted_data)

@bp.route('/report_personal_care')
def report_personal_care():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT timestamp, personal_care_type, personal_care_note, personal_care_duration, staff_initials
        FROM personal_care_chart
        WHERE resident_initials = ?
        ORDER BY timestamp DESC
    ''', (resident_initials,))
    personal_care_records = cursor.fetchall()
    conn.close()
    return render_template('report_personal_care.html', personal_care_records=personal_care_records, unit_name=unit_name, resident_initials=resident_initials)


@bp.route('/report_cardex')
def report_cardex():
    resident_initials = request.args.get('resident_initials')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT resident_initials, timestamp, cardex_text, staff_initials 
        FROM cardex 
        WHERE resident_initials = ? AND timestamp BETWEEN ? AND ?
        ORDER BY timestamp ASC
    ''', (resident_initials, start_date + ' 00:00:00', end_date + ' 23:59:59'))
    data = cursor.fetchall()
    conn.close()

    # Convert timestamp strings to datetime objects
    formatted_data = []
    for row in data:
        row = list(row)
        row[1] = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')  # Format without seconds
        formatted_data.append(row)

    return render_template('report_cardex.html', data=formatted_data)