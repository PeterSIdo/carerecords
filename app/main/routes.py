from flask import render_template, session, redirect, url_for, flash, request
from app.main import bp
import sqlite3

@bp.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        username = session.get('username', 'Guest')
        return render_template('index.html', username=username)
    return render_template('login.html')

@bp.route('/admin_panel')
def admin_panel():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        return render_template('admin_panel.html')
    return redirect(url_for('login.login'))

@bp.route('/enter_resident', methods=['GET', 'POST'])
def enter_resident():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        if request.method == 'POST':
            # Handle form submission for new resident
            pass
        return render_template('enter_resident.html')
    return redirect(url_for('login.login'))

@bp.route('/enter_service_list', methods=['GET', 'POST'])
def enter_service_list():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        if request.method == 'POST':
            # Handle form submission for service list
            pass
        return render_template('enter_service_list.html')
    return redirect(url_for('login.login'))

@bp.route('/enter_fluid_list', methods=['GET', 'POST'])
def enter_fluid_list():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        if request.method == 'POST':
            # Handle form submission for fluid list
            pass
        return render_template('enter_fluid_list.html')
    return redirect(url_for('login.login'))

@bp.route('/enter_food_list', methods=['GET', 'POST'])
def enter_food_list():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        if request.method == 'POST':
            # Handle form submission for food list
            pass
        return render_template('enter_food_list.html')
    return redirect(url_for('login.login'))

@bp.route('/enter_care_list', methods=['GET', 'POST'])
def enter_care_list():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        if request.method == 'POST':
            # Handle form submission for care list
            pass
        return render_template('enter_care_list.html')
    return redirect(url_for('login.login'))

@bp.route('/enter_bowel_list', methods=['GET', 'POST'])
def enter_bowel_list():
    if 'logged_in' in session and session['logged_in'] and session.get('user_mode') == 'a':
        if request.method == 'POST':
            # Handle form submission for bowel list
            pass
        return render_template('enter_bowel_list.html')
    return redirect(url_for('login.login'))

@bp.route('/manage_database', methods=['GET', 'POST'])
def manage_database():
    if request.method == 'POST':
        # Get form data
        resident_name = request.form.get('resident_name')
        unit_name = request.form.get('unit_name')
        room_nr = request.form.get('room_nr')
        service_list = request.form.get('service_list')
        fluid_list = request.form.get('fluid_list')
        food_list = request.form.get('food_list')
        care_list = request.form.get('care_list')
        bowel_list = request.form.get('bowel_list')

        # Connect to the database
        conn = sqlite3.connect('care4.db')
        cursor = conn.cursor()

        # Create tables if they do not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS resident_name (id INTEGER PRIMARY KEY, name TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS unit_name (id INTEGER PRIMARY KEY, name TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS room_nr (id INTEGER PRIMARY KEY, number INTEGER)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS service_list (id INTEGER PRIMARY KEY, service TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS fluid_list (id INTEGER PRIMARY KEY, fluid TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS food_list (id INTEGER PRIMARY KEY, food TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS care_list (id INTEGER PRIMARY KEY, care TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS bowel_list (id INTEGER PRIMARY KEY, bowel TEXT)''')

        # Insert data into tables only if the fields are not empty
        if resident_name:
            cursor.execute('INSERT INTO resident_name (name) VALUES (?)', (resident_name,))
        if unit_name:
            cursor.execute('INSERT INTO unit_name (name) VALUES (?)', (unit_name,))
        if room_nr:
            cursor.execute('INSERT INTO room_nr (number) VALUES (?)', (room_nr,))
        if service_list:
            cursor.execute('INSERT INTO service_list (service) VALUES (?)', (service_list,))
        if fluid_list:
            cursor.execute('INSERT INTO fluid_list (fluid) VALUES (?)', (fluid_list,))
        if food_list:
            cursor.execute('INSERT INTO food_list (food) VALUES (?)', (food_list,))
        if care_list:
            cursor.execute('INSERT INTO care_list (care) VALUES (?)', (care_list,))
        if bowel_list:
            cursor.execute('INSERT INTO bowel_list (bowel) VALUES (?)', (bowel_list,))

        # Commit changes and close connection
        conn.commit()
        conn.close()

        flash('Database updated successfully!')
        return redirect(url_for('main.manage_database'))

    return render_template('manage_database.html')