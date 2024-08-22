from flask import render_template, request, redirect, url_for, flash
from app.staff_log import bp
import sqlite3
from datetime import datetime
import uuid

@bp.route('/create_staff_log_tab', methods=['POST'])
def create_staff_log_tab():
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS staff_log (
            id TEXT PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            entry_category TEXT,
            description TEXT,
            suggested_completion_time DATETIME,
            initiator TEXT,
            completer TEXT
        )
    ''')  
    conn.commit()
    conn.close()
    flash('Staff log table created successfully!', 'success')
    return redirect(url_for('staff_log.view_staff_log'))

@bp.route('/create_staff_log', methods=['GET', 'POST'])
def create_staff_log():
    if request.method == 'POST':
        entry_category = request.form['entry_category']
        description = request.form['description']
        suggested_completion_time = request.form['suggested_completion_time']
        initiator = request.form['initiator']
        completer = request.form.get('completer', '')

        conn = sqlite3.connect('care4.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO staff_log (id, timestamp, entry_category, description, suggested_completion_time, initiator, completer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (str(uuid.uuid4()), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), entry_category, description, suggested_completion_time, initiator, completer))
        conn.commit()
        conn.close()

        flash('New staff log entry created successfully!', 'success')
        return redirect(url_for('staff_log.view_staff_log'))

    return render_template('create_staff_log.html')

@bp.route('/view_staff_log')
def view_staff_log():
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM staff_log')
    logs = cursor.fetchall()
    conn.close()
    return render_template('view_staff_log.html', logs=logs)

from flask import request, redirect, url_for, flash

from flask import request, redirect, url_for, flash
import sqlite3
from datetime import datetime
import uuid

@bp.route('/submit_staff_log', methods=['POST'])
def submit_staff_log():
    # Extract data from the form
    entry_category = request.form['entry_category']
    description = request.form['description']
    suggested_completion_time = request.form['suggested_completion_time']
    initiator = request.form['initiator']
    completer = request.form.get('completer', '')

    # Generate a timestamp for the current date and time
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Database insertion logic
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO staff_log (timestamp, entry_category, description, suggested_completion_time, initiator, completer)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (current_timestamp, entry_category, description, suggested_completion_time, initiator, completer))
    conn.commit()
    conn.close()

    flash('New staff log entry created successfully!', 'success')
    return redirect(url_for('staff_log.view_staff_log'))

@bp.route('/update_staff_log/<log_id>', methods=['GET', 'POST'])
def update_staff_log(log_id):
    if request.method == 'POST':
        completer = request.form['completer']
        task_completed = request.form.get('task_completed', 'off') == 'on'

        conn = sqlite3.connect('care4.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE staff_log
            SET completer = ?, task_completed = ?
            WHERE id = ?
        ''', (completer, task_completed, log_id))
        conn.commit()
        conn.close()

        flash('Staff log entry updated successfully!', 'success')
        return redirect(url_for('staff_log.view_staff_log'))

    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM staff_log WHERE id = ?', (log_id,))
    log = cursor.fetchone()
    conn.close()

    return render_template('update_staff_log.html', log=log)