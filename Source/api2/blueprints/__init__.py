from flask import Blueprint, g, session, request, jsonify

api2 = Blueprint('api2', __name__, template_folder='templates',url_prefix='/api2')

@api2.before_request
def before_request():
    print(request)

from . import system_mission, presets, gen_mission_status