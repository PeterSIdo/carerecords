# c:/Users/Peter/Documents/Care-Home-4/app/data_collection/routes.py
from flask import render_template, request, redirect, url_for, flash
from app.data_collection import bp
import sqlite3
from datetime import datetime

@bp.route('/collect_data')
def collect_data():
    resident_initials = request.args.get('resident_initials')
    service_name = request.args.get('service_name')
    return render_template('collect_data.html', resident_initials=resident_initials, service_name=service_name)


@bp.route('/data_collection_logic', methods=['POST'])
def data_collection_logic():
    resident_initials = request.form.get('resident_initials')
    service_name = request.form.get('service_name')
    if service_name == 'fluid intake':
        return redirect(url_for('data_collection.fluid_intake', resident_initials=resident_initials))
    elif service_name == 'food intake':
        return redirect(url_for('data_collection.food_intake', resident_initials=resident_initials))
    else:
            return redirect(url_for('data_collection.collect_data'))

@bp.route('/fluid_intake')
def fluid_intake():
    resident_initials = request.args.get('resident_initials')
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, fluid_name FROM fluid_list')
    fluid_list = cursor.fetchall()
    conn.close()
    return render_template('fluid_intake_form.html', fluid_list=fluid_list, resident_initials=resident_initials)

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