#C:\Users\Peter\Documents\Care-Home-4\app\dashboards\__init__.py
from flask import Blueprint

bp = Blueprint('dasboards', __name__)

from app.dashboards import routes