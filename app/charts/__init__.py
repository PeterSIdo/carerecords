#C:\Users\Peter\Documents\Care-Home-4\app\charts\__init__.py
from flask import Blueprint

bp = Blueprint('charts', __name__)

from app.charts import routes