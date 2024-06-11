# c:/Users/Peter/Documents/Care-Home-4/app/data_collection/routes.py
from flask import render_template, request
from app.data_collection import bp

@bp.route('/collect_data')
def collect_data():
    resident_initials = request.args.get('resident_initials')
    service_name = request.args.get('service_name')
    return render_template('collect_data.html', resident_initials=resident_initials, service_name=service_name)
    
        