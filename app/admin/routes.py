from flask import render_template, request, redirect, url_for, flash, session
from app.admin import bp
import sqlite3
from datetime import datetime
from app.login_check import login_required

@bp.route('/admin_dashboard')
@login_required(user_mode='a')
def admin_dashboard():
    return render_template('admin_dashboard.html')

# Add more admin routes here