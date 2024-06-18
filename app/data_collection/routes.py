# c:/Users/Peter/Documents/Care-Home-4/app/data_collection/routes.py
from flask import render_template, request, redirect, url_for, flash, session
from app.data_collection import bp
import sqlite3
from datetime import datetime
from app.login_check import login_required

@bp.route('/collect_data')
@login_required()
def collect_data():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    first_name = request.args.get('first_name')
    service_name = request.args.get('service_name')
    return render_template('collect_data.html', unit_name=unit_name, resident_initials=resident_initials, first_name=first_name, service_name=service_name)

@bp.route('/select_unit')
def select_unit():
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT unit_name FROM units')
    units = cursor.fetchall()
    conn.close()
    return render_template('select_unit.html', units=units)


@bp.route('/select_resident', methods=['POST'])
def select_resident():
    unit_name = request.form.get('unit_name')
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT resident_initials, first_name FROM residents WHERE unit_name = ?', (unit_name,))
    residents = cursor.fetchall()
    conn.close()
    return render_template('select_resident.html', residents=residents, unit_name=unit_name)

# c:/Users/Peter/Documents/Care-Home-4/app/data_collection/routes.py

@bp.route('/data_collection_logic', methods=['POST'])
def data_collection_logic():
    unit_name = request.form.get('unit_name')
    resident_initials = request.form.get('resident_initials')
    service_name = request.form.get('service_name')
    first_name= request.form.get('first_name')
    if service_name == 'fluid intake':
        return redirect(url_for('data_collection.fluid_intake', unit_name=unit_name, resident_initials=resident_initials))
    elif service_name == 'food intake':
        return redirect(url_for('data_collection.food_intake', unit_name=unit_name, resident_initials=resident_initials))
    else:
        return redirect(url_for('data_collection.collect_data'))

@bp.route('/fluid_intake')
def fluid_intake():
    unit_name = request.args.get('unit_name')
    resident_initials = request.args.get('resident_initials')
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, fluid_name FROM fluid_list')
    fluid_list = cursor.fetchall()
    conn.close()
    return render_template('fluid_intake_form.html', fluid_list=fluid_list, unit_name=unit_name, resident_initials=resident_initials)

@bp.route('/submit_fluid_intake', methods=['POST'])
def submit_fluid_intake():
    resident_initials = request.form.get('resident_initials')
    fluid_type = request.form.get('fluid_type')
    fluid_volume = request.form.get('fluid_volume')
    fluid_note = request.form.get('fluid_note')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fluid_chart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resident_initials TEXT,
            timestamp TEXT,
            fluid_type TEXT,
            fluid_volume INTEGER,
            fluid_note TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO fluid_chart (resident_initials, timestamp, fluid_type, fluid_volume, fluid_note)
        VALUES (?, ?, ?, ?, ?)
    ''', (resident_initials, timestamp, fluid_type, fluid_volume, fluid_note))
    conn.commit()
    conn.close()

    flash('The database was updated successfully!', 'success')
    return redirect(url_for('main.carer_input'))