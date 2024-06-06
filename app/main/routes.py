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