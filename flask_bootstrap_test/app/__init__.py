# app/__init__.py
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from app.decorators import login_required

def create_app():
    app = Flask(__name__)
    Bootstrap5(app)  # Initialize Bootstrap-Flask

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/carer_input')
    def carer():
        return render_template('carer.html')

    return app