import sqlalchemy, os, sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect

basedir = os.path.abspath(os.path.dirname(__file__))
if sys.platform.startswith('win'):
    sep = '\\'
else:
    sep = '/'

sys.path.append(basedir + sep + 'Model')

def create_process_app(db):
    process_app = Flask(__name__)
    process_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    process_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(process_app)
    # process_app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://dvirh:dvirh@localhost:3306/octopusdb4"
    
    return process_app

def create_app(db):
    app = Flask(__name__)
    db.init_app(app)
    return app

db = SQLAlchemy()
