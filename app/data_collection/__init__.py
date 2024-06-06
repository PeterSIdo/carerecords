# c:/Users/Peter/Documents/Care-Home-4/app/data_collection/__init__.py
from flask import Blueprint

bp = Blueprint('data_collection', __name__)

from app.data_collection import routes