#C:\Users\Peter\Documents\Care-Home-4\login\routes.py
#login\routes.py
from flask import render_template, redirect, url_for, flash, session
from app.login import bp
from app.login.forms import LoginForm
from app.login.login_evaluation import evaluate_login

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_mode = form.user_mode.data
        username = form.username.data
        password = form.password.data
        if evaluate_login(username, password):
            session['user_mode'] = user_mode
            session['logged_in'] = True
            session['username'] = username
            if user_mode == 'a': 
                return redirect(url_for('main.admin_panel'))
            if user_mode == 'c':
                return redirect(url_for('charts.charts_menu'))
            
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)