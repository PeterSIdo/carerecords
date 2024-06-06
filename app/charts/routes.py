# C:\Users\Peter\Documents\Care-Home-4\app\charts\routes.py
# \charts\routes.py

from flask import render_template
from app.charts import bp

@bp.route('/charts_menu')
def charts_menu():
    return render_template('charts_menu.html')


@bp.route('/fluid_chart')
def fluid_chart():
    return render_template('fluid_chart.html')

@bp.route('/food_chart')
def food_chart():
    return render_template('food_chart.html')