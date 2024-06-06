# C:\Users\Peter\Documents\Care-Home-4\login\__init__.py
from flask import Blueprint

bp = Blueprint('login', __name__)

from app.login import routes, login_evaluation