from flask import Blueprint, render_template, abort, jsonify, session
from jinja2 import TemplateNotFound
import json, os
dummy = Blueprint('dummy', __name__,
                        template_folder='templates')

@dummy.route('/dummyapi/RunMission/get_by_id/<int:mission_id>')
def RunMission(mission_id):
    basedir = os.path.abspath(os.path.dirname(__file__))
    json_data = json.load(open(basedir+f"\\dummy_run_mission_{mission_id}.json",'r'))
    return json_data, 200

@dummy.route('/dummyapi/GenerateMission/get_by_id/<int:mission_id>')
def GenerateMission(mission_id):
    json_data = json.load(open(f"dummy_generate_mission_{mission_id}.json",'r'))
    return json_data, 200
