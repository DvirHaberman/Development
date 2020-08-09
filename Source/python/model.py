##################################################################################################
### This model defines the ORM model classes inheriting from flask_sqlalchemy db.Model         ###
### The classes contains one-to-one, one-to-man and many-to-many relationships                 ###
### It is advised to have a firm knowledge of these relationships before committing any changes ###
##################################################################################################


import pandas as pd
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, request, jsonify, render_template, session, flash
import json
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from time import time, sleep
import importlib
from pathlib import Path
import sys
import os
from os import listdir
from os.path import isfile, join
import cx_Oracle
from time import time
from decimal import Decimal
import re

if sys.platform.startswith('win'):
    sep = '\\'
else:
    sep = '/'

def run_sql(conn, run_id, query, params):
    try:
        translator = {"&run_id":run_id}
        for index, row in params.iterrows():
            translator['&' + row.param_name] = row.value
    except:
        return {
                    'result_status':1,
                    'result_text':"Error! parameters extaction error!",
                    'results_arr' : None
                }

    try:
        for key, value in translator.items():
            query = query.replace(key,str(value))
    except:
        return {
                    'result_status':1,
                    'result_text':"Error! parameters replacement error!",
                    'results_arr' : None
                }
    try:
        result = pd.read_sql(query,con=conn)
        result['status'] = 4
        result['text'] = 'some text'
    except Exception as error:
        return {
                        'result_status':1,
                        'result_text':"Error! SQL didn't run properly!",
                        'results_arr' : None
                    }
    if len(result) == 0:
        return {
                        'result_status':1,
                        'result_text':'Error! SQL returned an empty result',
                        'results_arr' : None
        }

    try:
        if len(result) > 0:
            result_status = list(result.head(1)['status'].values)[0]
            result_text = list(result.head(1)['text'].values)[0]
            result.drop(columns=['status', 'text'], inplace=True)
            return {
                            # 'result_status':result_first_line['Status'],
                            # 'result_text':result_first_line['Text'],
                            'result_status':result_status,
                            'result_text': result_text,
                            'results_arr' : result
                        }
    except Exception as error:
        return {
                    'result_status':1,
                    'result_text':"Error! something went wrong while extracting the result Text, Status and array",
                    'results_arr' : None
                }


def run_matlab(conn, run_id, params):
    return {
        'result_status':4,
        'result_text':"Well you just did nothing",
        'results_arr' : None
    }

def init_db():
    db = SQLAlchemy()
    return db

def create_process_app(db):
    process_app = Flask(__name__)
    db.init_app(process_app)
    # process_app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://dvirh:dvirh@localhost:3306/octopusdb4"
    process_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    process_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return process_app

def create_app(db):
    app = Flask(__name__)
    db.init_app(app)
    return app

db = init_db()

FunctionsAndGroups = db.Table('FunctionsAndGroups',
                              db.Column('function_id', db.Integer,
                                        db.ForeignKey('OctopusFunctions.id')),
                              db.Column('group_id', db.Integer,
                                        db.ForeignKey('FunctionsGroup.id'))
                              )

ProjectsAndUsers = db.Table('ProjectsAndUsers',
                              db.Column('project_id', db.Integer,
                                        db.ForeignKey('Project.id')),
                              db.Column('user_id', db.Integer,
                                        db.ForeignKey('User.id'))
                              )

SetupsAndFunctions = db.Table('SetupsAndFunctions',
                              db.Column('setup_id', db.Integer,
                                        db.ForeignKey('AnalyseSetup.id')),
                              db.Column('function_id', db.Integer,
                                        db.ForeignKey('OctopusFunctions.id'))
                              )

SetupsAndGroups = db.Table('SetupsAndGroups',
                              db.Column('setup_id', db.Integer,
                                        db.ForeignKey('AnalyseSetup.id')),
                              db.Column('group_id', db.Integer,
                                        db.ForeignKey('FunctionsGroup.id'))
                              )

SetupsAndRunLists = db.Table('SetupsAndRunLists',
                              db.Column('setup_id', db.Integer,
                                        db.ForeignKey('AnalyseSetup.id')),
                              db.Column('run_list_id', db.Integer,
                                        db.ForeignKey('RunList.id'))
                              )

SetupsAndRuns = db.Table('SetupsAndRuns',
                              db.Column('setup_id', db.Integer,
                                        db.ForeignKey('AnalyseSetup.id')),
                              db.Column('run_id', db.Integer,
                                        db.ForeignKey('SetupRuns.id'))
                              )

################################################
########### DBCONNECTOR CLASS ###############
################################################

class DbConnector:

    def __init__(self, db_type, user, password, hostname, schema, port=None, name=None):

        # setting up propeties
        self.db_type = db_type
        self.schema = schema
        self.user = user
        self.password = password
        self.hostname = hostname
        self.port = port
        self.connection = None
        self.message = ''

        # assinging name - if no name is given then the name is composed of the type and schema
        if name or name == '':
            self.name = name
        else:
            self.name = self.db_type + self.schema

        # checking db type
        if self.port == '':
            if db_type == 'ORACLE':
                self.conn_string =f"oracle+cx_oracle://{self.user}:{self.password}@{self.hostname}/{self.schema}"
            elif db_type == 'SQLITE':
                self.conn_string = f'sqlite://{self.user}:{self.password}@{self.hostname}/{self.schema}'
            elif db_type == 'POSTGRESQL':
                self.conn_string = f"postgresql://{self.user}:{self.password}@{self.hostname}/{self.schema}"
            elif db_type == 'MYSQL':
                self.conn_string = f'mysql+mysqlconnector://{self.user}:{self.password}@{self.hostname}/{self.schema}'
            else:
                self.conn_string = None
                self.message = 'Database type not found. Possible types are :\n'
                'ORACLE, SQLITE, POSTGRESQL, MYSQL'
        else:
            if db_type == 'ORACLE':
                self.conn_string =f"oracle+cx_oracle://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.schema}"
            elif db_type == 'SQLITE':
                self.conn_string = f'sqlite://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.schema}'
            elif db_type == 'POSTGRESQL':
                self.conn_string = f"postgresql://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.schema}"
            elif db_type == 'MYSQL':
                self.conn_string = f'mysql+mysqlconnector://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.schema}'
            else:
                self.conn_string = None
                self.message = 'Database type not found. Possible types are :\n'
                'ORACLE, SQLITE, POSTGRESQL, MYSQL'
        # checking if we have a connection string and can try to connect
        if self.conn_string:
            try:
                self.connection = create_engine(self.conn_string, connect_args={'connect_timeout': 5})
                conn = self.connection.connect()
                conn.close()
                self.connection.dispose()
                self.connection = None
            except Exception as error:
                self.message = 'Someting went wrong while trying to connect.'
                try:
                    self.connection.dispose()
                except Exception as error:
                    pass
        # setting the connection status
        if self.message == '':
            self.status = 'valid'
        else:
            self.status = 'invalid'

    def save(self):
        # checking id connectiong is valid - cannot save invalid connection
        if self.status == 'invalid':
            self.message = 'Cannot save invalid connection'
            return

        # checking if the name exists - names must be unique
        if DbConnections.query.filter_by(name=self.name,project=session['current_project_id']).first():
            self.message = 'cannot save - db name already exist'
            self.status = 'invalid'
            return
        # saving connection data to DB
        try:
            conn = DbConnections(self.db_type, self.user, self.password, self.hostname,
                                 self.port, self.schema, self.name, self.conn_string, project=session['current_project_id'])
            db.session.add(conn)
            db.session.commit()
        except Exception as error:
            self.message = 'Something when wrong while saving to DB.'
            self.status = 'invalid'

    def run_sql(self,sql):
        if self.status == 'valid':
            self.connection = create_engine(self.conn_string, connect_args={'connect_timeout': 5})
            conn = self.connection.connect()
            data = pd.read_sql(sql,con=conn)
            conn.close()
            self.connection.dispose()
            self.connection = None
            return data
        else:
            return 'invalid conn'

    @staticmethod
    def load_conn_by_id(conn_id=1):
        conn_data = DbConnections.query.get(conn_id)
        return DbConnector(db_type=conn_data.db_type, user=conn_data.user,
                         password=conn_data.password, hostname=conn_data.hostname,
                         schema=conn_data.schema, port=conn_data.port,
                         name=conn_data.name)

    @staticmethod
    def load_conn_by_name(db_name):
        conn_data = DbConnections.query.filter_by(name=db_name,project=session['current_project_id']).first()
        if conn_data:
            return DbConnector(db_type=conn_data.db_type, user=conn_data.user,
                            password=conn_data.password, hostname=conn_data.hostname,
                            schema=conn_data.schema, port=conn_data.port,
                            name=conn_data.name)
        else:
            return DbConnector(db_type='', user='',
                            password='', hostname='',
                            schema='', port='',
                            name=db_name)
    @staticmethod
    def get_run_ids(db_name):
        conn = DbConnector.load_conn_by_name(db_name)
        data = conn.run_sql('select run_id, scenario_name from run_ids')
        return jsonify(status=1,run_ids=[int(x) for x in list(data["run_id"].values)],scenarios=list(data["scenario_name"].values))

    @staticmethod
    def get_run_ids_json(db_name):
        conn = DbConnector.load_conn_by_name(db_name)
        data = conn.run_sql('select run_id, scenario_name from run_ids')
        data_json = [{"run_id":row['run_id'], 'scenario_name':row["scenario_name"]} for _,row in data.iterrows()]
        return jsonify(status=1, data=data_json)

    @staticmethod
    def get_empty():
        return jsonify(status=1, data=[])


    @staticmethod
    def delete_conn_by_name(name):
        try:
            conn = DbConnections.query.filter_by(name=name,project=session['current_project_id']).first()
            if conn:
                db.session.delete(conn)
                db.session.commit()
                return jsonify(status=1,msg='Connection ' + name + ' succefully deleted')
            else:
                return jsonify(status=0,msg='Not deleted! No connection with this name')
        except:
            return jsonify(status=0,msg='Not deleted! Something went wrong in the delete process')

###########################################
########### OCTOPUSUTILS CLASS ############
###########################################


class OctopusUtils:

    @staticmethod
    def get_all_functions():
        functions = OctopusFunction.query.all()
        # owner_id = functions[0].owner
        # owner = User.query.get(owner_id).name
        # , owners=owner)
        return jsonify(names=[func.name for func in functions])

    @staticmethod
    def get_sys_params(conn, run_id):
        return pd.read_sql('select * from sys_params',con=conn)
        # return pd.read_sql(f'select * from sys_params where run_id={run_id}',con=conn)

    @staticmethod
    def get_test_params():
        return 'Tests Params'

    @staticmethod
    def get_db_conn(db_name):
        return 'db_conn for'+ db_name

    @staticmethod
    def get_files_in_dir(json_data):
        base_path = sep.join(json_data['path'].split(sep)[0:-1]+[''])
        return jsonify(all=[join(base_path, f) for f in listdir(base_path)], files=[f for f in listdir(base_path) if isfile(join(base_path, f))])

    @staticmethod
    def get_functions_basedir():
        basedir = os.path.abspath(os.path.dirname(__file__))
        return jsonify(dir=sep.join(basedir.split(sep)[0:-2]+['Functions','']))



########################################
########### TASK CLASS ############
########################################


class Task:

    def __init__(self, mission_id, db_conn_obj, run_id, run_status, scenario_name, function_id, user_id, task_id=0, priority=1, status=0):
        self.id=task_id
        self.mission_id=mission_id
        self.db_conn_obj = db_conn_obj
        self.run_id = run_id
        self.run_status = run_status
        self.scenario_name = scenario_name
        self.function_id = function_id
        self.user_id = user_id
        self.priority = priority
        self.status = status

    def log(self):
        task = AnalyseTask(mission_id=self.mission_id, mission_type=0, function_id=self.function_id,
                 run_id=self.run_id, run_status=self.run_status, scenario_name=self.scenario_name, scenario_id=None, ovr_file_location=None, db_conn_string=self.db_conn_obj.name,
                 priority=1, user_id=self.user_id, status=-3)
        db.session.add(task)
        db.session.commit()
        self.id = task.id

    # def log_result(self, results):
    #     analyse_result = AnalyseResult(task_id=self.id,run_id=results['run_id'],
    #                                 db_conn_string=self.db_conn_obj.conn_string,
    #                                 result_status=results['result_status'],
    #                                 result_text=results['result_text'],
    #                                 result_array=results['result_arr'])
    #     db.session.add(analyse_result)
    #     db.session.commit()

    def run(self):
        function_obj = OctopusFunction.query.get(self.function_id)
        result_dict = self.function_obj.run(self.db_conn_obj, self.run_id)
        self.status = result_dict['result_status']
    def update(self):
        task = AnalyseTask.query.filter_by(id=self.id).first()
        task.status = self.status
        db.session.add(task)
        db.session.commit()

#########################################
########### TEAM MODEL CLASS ############
#########################################

class Team(db.Model):
    __tablename__ = "Team"
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', backref='Team', lazy=True, uselist=True)
    name = db.Column(db.Text)

    def __init__(self, name=None, users=[]):
        self.name = name
        self.users = users

    def self_jsonify(self):
        return jsonify(
            name=self.name,
            users=jsonify([user.self_jsonify() for user in self.users]).json
        ).json

    @staticmethod
    def jsonify_all():
        table = Team.query.all()
        return jsonify([row.self_jsonify() for row in table])

    @staticmethod
    def get_names():
        names = Team.query.with_entities(Team.name).all()
        return jsonify(list(*zip(*names)))

#########################################
########### ROLE MODEL CLASS ############
#########################################


class Role(db.Model):
    __tablename__ = 'Role'
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', backref='Role', lazy=True, uselist=True)
    name = db.Column(db.Text)

    def __init__(self, name=None, users=[]):
        self.name = name
        self.users = users

    def self_jsonify(self):
        return jsonify(
            name=self.name,
            users=jsonify([user.self_jsonify() for user in self.users]).json
        ).json

    @staticmethod
    def jsonify_all():
        table = Role.query.all()
        return jsonify([row.self_jsonify() for row in table])

    @staticmethod
    def get_names():
        names = Role.query.with_entities(Role.name).all()
        return jsonify(list(*zip(*names)))


#########################################
########### USER MODEL CLASS ############
#########################################

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    password_sha = db.Column(db.Text)
    role = db.Column(db.Integer, db.ForeignKey('Role.id'))
    team = db.Column(db.Integer, db.ForeignKey('Team.id'))
    functions = db.relationship('OctopusFunction', backref='User', lazy=True)
    max_priority = db.Column(db.Integer)
    state = db.Column(db.Integer)
    # project = db.Column(db.Integer, db.ForeignKey('Project.id'))
    projects = db.relationship('Project', secondary=ProjectsAndUsers,
                                backref=db.backref('users', lazy='dynamic'))
    default_project = db.Column(db.Integer)

    def __init__(self, name=None, first_name=None, last_name=None, password_sha=None, state=None,
                 role=None, team=None, functions=[], max_priority=None, projects=[], default_project=None):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.password_sha = password_sha
        self.state = state
        self.role = role
        self.team = team
        self.functions = functions
        self.max_priority = max_priority
        self.projects = projects
        self.default_project = default_project

    def self_jsonify(self):
        return jsonify(
            name=self.name,
            first_name=self.first_name,
            last_name=self.last_name,
            password_sha=self.password_sha,
            state=self.state,
            role=self.Role.query.get(self.role).name,
            team=self.Team.query.get(self.team).name,
            functions=jsonify([func.self_jsonify()
                               for func in self.functions]).json,
            max_priority=self.max_priority,
            projects=jsonify([project.name
                               for project in self.projects]).json
        ).json

    @staticmethod
    def save_user(data):
        status = 0
        if len(data['first_name']) == 0 or len(data['last_name']) == 0:
            return jsonify(status=status,msg='user first and last name must not be empty')
        if len(data['max_priority']) == 0:
            return jsonify(status=status,msg='user max priority must not be empty')
        if not (data['max_priority']).isdigit():
            return jsonify(status=status,msg='user max priority must be a number')
        user = User.query.filter_by(first_name=data['first_name'], last_name=data['last_name']).all()
        if len(user) > 0:
            return jsonify(status=status,msg='user with this name already exist')
        k=0
        while len(User.query.filter_by(name = data['first_name']+data['last_name'][:k+1]).all())>0:
            k+=1
        team_id = Team.query.filter_by(name=data['team']).first().id
        role_id = Role.query.filter_by(name=data['role']).first().id
        projects = db.session.query(Project).filter(Project.name.in_(data['projects'])).all()
        user = User(name=data['first_name']+data['last_name'][:k+1], first_name=data['first_name'], last_name=data['last_name'], password_sha='123456', state=0,
                 role=role_id, team=team_id, functions=[], max_priority=int(data['max_priority']), projects=projects)
        db.session.add(user)
        db.session.commit()
        session['projects'] = data['projects']
        if session['projects']:
            if session['current_project'] not in session['projects']:
                session['current_project'] = session['projects'][0]
        else:
            session['current_project'] = None

        return jsonify(status=1, msg='user ' + user.name +' was successfuly saved')

    @staticmethod
    def update_user(data):
        user = User.query.get(int(data['id']))
        user.max_priority = data['max_priority']
        user.team = Team.query.filter_by(name=data['team']).first().id
        user.role = Role.query.filter_by(name=data['role']).first().id
        user.projects = []
        user.projects = db.session.query(Project).filter(Project.name.in_(data['projects'])).all()
        db.session.add(user)
        db.session.commit()
        session['projects'] = data['projects']
        if session['projects']:
            if session['current_project'] not in session['projects']:
                session['current_project'] = session['projects'][0]
        else:
            session['current_project'] = None
        return jsonify(status=1,msg='user updated!')
    @staticmethod
    def delete_user_by_name(name):
        try:
            user = User.query.filter_by(name=name).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                return jsonify(status=1,msg='User succefully deleted')
            else:
                return jsonify(status=0,msg='Not deleted! No user with this name')
        except:
            return jsonify(status=0,msg='Not deleted! Something went wrong in the delete process')

    @staticmethod
    def delete_user_by_id(user_id):
        try:
            user = User.query.get(int(user_id))
            db.session.delete(user)
            db.session.commit()
            return jsonify(status=1,msg='User succefully deleted')
        except:
            return jsonify(status=0,msg='Not deleted! Something went wrong in the delete process')

    @staticmethod
    def reset_password_by_name(user_id):
        try:
            user = User.query.filter_by(name=name).first()
            if user:
                user.password_sha = '123456'
                db.session.add(user)
                db.session.commit()
                return jsonify(status=1,msg='Pasword resetted')
            else:
                return jsonify(status=0,msg='Not resetted! No user with this name')
        except:
            return jsonify(status=0,msg='Not resetted! Something went wrong in the reset process')

    @staticmethod
    def reset_password_by_id(user_id):
        try:
            user = User.query.get(int(user_id))
            user.password_sha = '123456'
            db.session.add(user)
            db.session.commit()
            return jsonify(status=1,msg='Pasword resetted')
        except:
            return jsonify(status=0,msg='Not resetted! Something went wrong in the reset process')

    @staticmethod
    def jsonify_all():
        table = User.query.all()
        return jsonify([row.self_jsonify() for row in table])

    @staticmethod
    def get_names():
        try:
            names = User.query.with_entities(User.name).all()
            names = list(*zip(*names))
            status = 1
            
        except:
            names = []
            status = 0
        return jsonify(status=status, data=names)
    @staticmethod
    def get_names_and_ids():
        users = User.query.with_entities(User.name, User.id).all()
        names = [user.name for user in users]
        ids = [user.id for user in users]
        return jsonify(names=names, ids=ids)

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(int(user_id))
        return jsonify(user.self_jsonify())

    # def __repr__(self):
    #     print(f'my name is {self.name} and my function are:')
    #     for func in self.functions:
    #         print(func.printme())

    # def printme(self):
    #     str1 = f'my name is {self.name} and my function are:'
    #     for func in self.Functions:
    #         str1 = str1 + func.printme()
    #     return str1


##########################################
######### PROJECT MODEL CLASS ############
##########################################


class Project(db.Model):
    __tablename__ = 'Project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    output_dir = db.Column(db.Text)
    repository_root = db.Column(db.Text)
    # users = db.relationship('User', backref='Project', lazy=True)
    sites = db.relationship('Site', backref='Project', lazy=True)
    functions = db.relationship(
        'OctopusFunction', backref='Project', lazy=True, uselist=True)
    functions_groups = db.relationship(
        'FunctionsGroup', backref='Project', lazy=True, uselist=True)
    db_connections = db.relationship(
        'DbConnections', backref='Project', lazy=True, uselist=True)

    def __init__(self, name, output_dir=None, repository_root=None, sites=[]):
        self.name = name
        # self.version = version
        self.output_dir = output_dir
        self.repository_root = repository_root
        # self.users = users
        self.sites = sites

    def self_jsonify(self):
        return jsonify(
            id=self.id,
            name=self.name,
            output_dir=self.output_dir,
            # users=jsonify([user.name for user in self.users]).json,
            users=jsonify([user.self_jsonify() for user in self.users]).json,
            sites=jsonify([site.self_jsonify() for site in self.sites]).json,
            sites_names=jsonify([site.name for site in self.sites]).json
        ).json

    @staticmethod
    def get_names():
        try:
            names = Project.query.with_entities(Project.name).all()
            return jsonify(status=1, message=None, data=list(*zip(*names)))
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def get_by_id(project_id):
        try:
            project = Project.query.get(int(project_id))
            return jsonify(status=1, message=None, data=project.self_jsonify())
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def get_by_name(project_id):
        try:
            project = Project.query.filter_by(name=project_id).first()
            return jsonify(status=1, message=None, data=project.self_jsonify())
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def save(json_data):
        try:
            if json_data['name'] in [project.name for project in Project.query.all()]:
                return jsonify(status=0, message='Not saved! a project with this name already exist')
            name = json_data['name']
            output_dir = json_data['output_dir']
            project = Project(name, output_dir)

            db.session.add(project)
            db.session.commit()

            return jsonify(status= 1, message='project '  + project.name + ' succesfully saved')
        except Exception as error:
            return jsonify(status=0, message='Not saved! something went wrong - please try again later')
        finally:
            db.session.close()

    @staticmethod
    def delete_by_name(name):
        try:
            project = Project.query.filter_by(name=name).first()
            if project:
                db.session.delete(project)
                db.session.commit()
                return jsonify(status=1,msg='project ' + name + ' succefully deleted')
            else:
                return jsonify(status=0,msg='Not deleted! No project with this name')
        except:
            return jsonify(status=0,msg='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def delete_by_id(project_id):
        try:
            project = Project.query.get(int(project_id))
            if project:
                db.session.delete(project)
                db.session.commit()
                return jsonify(status=1,msg='project ' + name + ' succefully deleted')
            else:
                return jsonify(status=0,msg='Not deleted! No project with this id')
        except:
            return jsonify(status=0,msg='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def update_by_name(name, json_data):
        try:
            project = Project.query.filter_by(name=name).first()
            if project:
                project.output_dir = json_data['output_dir']
                project.name = json_data['name']

                db.session.add(project)
                db.session.commit()
                return jsonify(status=1,message='project ' + project.name + ' succesfully updated')
            else:
                return jsonify(status=0,message='Not deleted! No project with this name')


            return jsonify(status= 1, message='project '  + project.name + ' succesfully updated')
        except Exception as error:
            return jsonify(status=0, message='Not updated! something went wrong - please try again later')
        finally:
            db.session.close()

    @staticmethod
    def update_by_id(project_id, json_data):
        try:
            project = Project.query.get(int(project_id))
            if project:
                project.output_dir = json_data['output_dir']
                project.name = json_data['name']

                db.session.add(project)
                db.session.commit()
                return jsonify(status=1,message='project ' + project.name + ' succefully updated')
            else:
                return jsonify(status=0,message='Not deleted! No project with this name')
            return jsonify(status= 1, message='project '  + project.name + ' succesfully updated')
        except Exception as error:
            return jsonify(status=0, message='Not updated! something went wrong - please try again later')
        finally:
            db.session.close()
#####################################################
######### FunctionParameters MODEL CLASS ############
#####################################################


class FunctionParameters(db.Model):
    __tablename__ = 'FunctionParameters'
    id = db.Column(db.Integer, primary_key=True)
    function_id = db.Column(db.Integer, db.ForeignKey('OctopusFunctions.id'))
    index = db.Column(db.Integer)
    kind = db.Column(db.Text)
    value = db.Column(db.Text)
    param_type = db.Column(db.Text)

    def __init__(self, function_id=None, index=None, kind=None, value=None, param_type=None):
        self.function_id = function_id
        self.index = index
        self.kind = kind
        self.value = value
        self.param_type = param_type

    def self_jsonify(self):
        return jsonify(
            function_id=self.function_id,
            index = self.index,
            kind=self.kind,
            value=self.value,
            type=self.param_type
        ).json

    @staticmethod
    def save(function_id=None, index=index, kind=None, value=None, param_type=None):
        param = FunctionParameters(function_id = function_id,
                                    index = index, kind = kind,
                                    value = value, param_type = param_type)
        db.session.add(param)
        db.session.commit()

    @staticmethod
    def jsonify_all():
        table = FunctionParameters.query.all()
        return jsonify([row.self_jsonify() for row in table])

    def get_value(self, conn, run_id):
        if self.kind == 'Sys Params':
            return OctopusUtils.get_sys_params(conn, run_id)

        if self.kind == 'Tests Params':
            return OctopusUtils.get_test_params()

        if self.kind == 'value':
            if self.type == 'int':
                if not type(self.value) == type(1):
                    if type(self.value) == type('str'):
                        return int(self.value.split('.')[0])
                    else:
                        return int(self.value)
                return self.value

            if self.type == 'string':
                if not type(self.value) == type('str'):
                    return str(self.value)
                return self.value

            if self.type == 'float':
                if not type(self.value) == type(1.7):
                    return float(self.value)
                return self.value

        return self.value
#####################################################
########### OCTOPUSFUNCTION MODEL CLASS ############
#####################################################


class OctopusFunction(db.Model):
    __tablename__ = "OctopusFunctions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    callback = db.Column(db.Text)
    file_name = db.Column(db.Text)
    location = db.Column(db.Text)
    owner = db.Column(db.Integer, db.ForeignKey('User.id'))
    status = db.Column(db.Integer)
    tree = db.relationship(
        'Trees', backref='OctopusFunction', lazy=True, uselist=False)
    kind = db.Column(db.Text)
    tags = db.Column(db.Text)
    description = db.Column(db.Text)
    is_class_method = db.Column(db.Integer)
    class_name = db.Column(db.Text)
    version = db.Column(db.Integer)
    version_comments = db.Column(db.Text)
    function_checksum = db.Column(db.Text)
    handler_checksum = db.Column(db.Text)
    changed_date = db.Column(db.DateTime)
    is_locked = db.Column(db.Integer)
    function_parameters = db.relationship(
        'FunctionParameters', backref='OctopusFunction', lazy=True, uselist=True)
    feature = db.Column(db.Text)
    requirement = db.Column(db.Text)
    project = db.Column(db.Integer, db.ForeignKey('Project.id'))
    changed_by = db.Column(db.Text)

    def __init__(self, name=None, callback=None, file_name=None, location=None, owner=None, status=None, tree=None,
                 kind=None, tags=None, description=None, version_comments=None,  is_class_method=1, class_name='Calc',
                 function_checksum=None, version=None, handler_checksum=None, function_parameters=[], changed_date=datetime.utcnow(),
                 is_locked=0, feature=None, requirement=None, project=None, changed_by=None):
        self.name = name
        self.file_name = file_name
        self.callback = callback
        self.location = location
        self.owner = owner
        self.status = status
        self.tree = tree
        self.kind = kind
        self.tags = tags
        self.description = description
        self.is_class_method = is_class_method
        self.class_name = class_name
        self.version = version
        self.version_comments = version_comments
        self.function_checksum = function_checksum
        self.handler_checksum = handler_checksum
        self.changed_date = changed_date
        self.is_locked = is_locked
        self.function_parameters = function_parameters
        self.feature = feature
        self.requirement = requirement
        self.project = project
        self.changed_by = changed_by

    def self_jsonify(self):
        try:
            owner = User.query.get(self.owner).name
        except:
            owner = self.owner
        try:
            tree = self.tree.self_jsonify()
        except:
            tree = None

        try:
            groups = jsonify([group.name for group in self.groups]).json
        except:
            groups = None

        return jsonify(
            id=self.id,
            name=self.name,
            callback=self.callback,
            file_name=self.file_name,
            location=self.location,
            owner=owner,
            status=self.status,
            tree=tree,
            kind=self.kind,
            tags=self.tags,
            description=self.description,
            is_class_method=self.is_class_method,
            class_name=self.class_name,
            groups=groups,
            version=self.version,
            version_comments=self.version_comments,
            function_checksum=self.function_checksum,
            handler_checksum=self.handler_checksum,
            changed_date=self.changed_date,
            is_locked=self.is_locked,
            feature = self.feature,
            requirement = self.requirement,
            changed_by = self.changed_by,
            function_parameters=jsonify([param.self_jsonify() for param in self.function_parameters]).json
        ).json

    @staticmethod
    def save_function(data):
        try:
            if data['name'] in [func.name for func in OctopusFunction.query.all()]:
                return jsonify(f"Couldn't save function - already exist")

            if data['is_class_method']:
                is_class_method=1
            else:
                is_class_method=0


            if 'status' in data:
                status = data['status']
            else:
                status = 0

            if 'groups' in data:
                groups = data['groups']
            else:
                groups = []

            if 'feature' in data:
                feature = data['feature']
            else:
                feature = None

            if 'requirement' in data:
                requirement = data['requirement']
            else:
                requirement = None

            if 'owner' in data:
                owner = User.query.filter_by(name=data['owner']).first()
                if owner:
                    owner = owner.id
                else:
                    owner=User.query.filter_by(name=session['username']).first().id
            else:
                owner=User.query.filter_by(name=session['username']).first().id

            func = OctopusFunction(
                name=data['name'],
                callback=data['callback'],
                location=data['location'],
                owner=owner,
                file_name = data['location'].split(sep)[-1],
                class_name = data['class_name'],
                is_class_method = is_class_method,
                status=status,
                # tree=row.tree,
                feature=feature,
                requirement=requirement,
                kind=data['kind'],
                tags=data['tags'],
                description=data['description'],
                project=session['current_project_id'],
                # version=data['version'],
                # version_comments=data['version_comments'],
                function_checksum=22,
                handler_checksum=33,
                changed_by = User.query.filter_by(name=session['username'])[0].name
                # is_locked=row.is_locked
            )
            db.session.add(func)
            db.session.commit()
        except Exception as error:
            return jsonify("Not Saved! Something went wrong while saving the functions")

        try:
            function_id = func.id
            for param in data['function_parameters']:
                index = param['index']
                kind = param['kind']
                value = param['value']
                param_type = param['type']
                FunctionParameters.save(function_id = function_id,
                                        index = index, kind = kind,
                                        value = value, param_type = param_type)

        except Exception as error:
            try:
                FunctionParameters.query.filter_by(function_id = func.id).delete()
                db.session.delete(func)
                db.session.commit()
                return jsonify(f"Not Saved! Something went wrong while saving the parameters")
            except:
                return jsonify(f"Not Saved! Something went wrong while saving the parameters")
        try:
            # function_id = func.id
            for group in groups:
                groupobj = FunctionsGroup.query.filter_by(name=group).first()
                if groupobj:
                    groupobj.functions.append(func)
                    db.session.add(groupobj)
                    db.session.commit()
            return jsonify(f"function {func.name} was succefully saved")
        except Exception as error:
            try:
                db.session.delete(func)
                db.session.commit()
                return jsonify(f"Not Saved! Something went wrong while saving the parameters")
            except:
                return jsonify(f"Not Saved! Something went wrong while saving the parameters")

    @staticmethod
    def update(data):
        try:
            try:
                if not data['name'] in [func.name for func in OctopusFunction.query.all()]:
                    return jsonify(f"No function with this name")

                if data['is_class_method']:
                    is_class_method=1
                else:
                    is_class_method=0


                if 'status' in data:
                    status = data['status']
                else:
                    status = 0

                if 'groups' in data:
                    groups = data['groups']
                else:
                    groups = []

                if 'feature' in data:
                    feature = data['feature']
                else:
                    feature = None

                if 'requirement' in data:
                    requirement = data['requirement']
                else:
                    requirement = None

                func = OctopusFunction.query.filter_by(name=data['name']).first()
                if 'owner' in data:
                    owner = User.query.filter_by(name=data['owner']).first()
                    if owner:
                        owner = owner.id
                    else:
                        owner = func.owner
                else:
                    owner = func.owner
                func.name=data['name']
                func.callback=data['callback']
                func.location=data['location']
                func.owner=owner
                func.file_name = data['location'].split(sep)[-1]
                func.class_name = data['class_name']
                func.is_class_method = is_class_method
                func.status=status
                # tree=row.tree,
                func.feature=feature
                func.requirement=requirement
                func.kind=data['kind']
                func.tags=data['tags']
                func.description=data['description']
                func.changed_date = datetime.utcnow()
                func.changed_by = User.query.filter_by(name=session['username'])[0].name
                # project=row.project,
                # func.version=data['version']
                # func.version_comments=data['version_comments']
                # func.function_checksum=22
                # func.handler_checksum=33
                # is_locked=row.is_locked
                # db.session.add(func)
                # db.session.commit()
            except Exception as error:
                # db.session.rollback()
                return jsonify("Not Saved! Something went wrong while saving the functions")

            try:
                [db.session.delete(param) for param in func.function_parameters]
                function_id = func.id
                for param in data['function_parameters']:
                    index = param['index']
                    kind = param['kind']
                    value = param['value']
                    param_type = param['type']
                    FunctionParameters.save(function_id = function_id,
                                            index = index, kind = kind,
                                            value = value, param_type = param_type)

            except Exception as error:
                # db.session.rollback()
                return jsonify(f"Not Saved! Something went wrong while saving the parameters")
            try:
                func.groups = []
                func.groups = [FunctionsGroup.query.filter_by(name=group).first() for group in groups]
                # for group in groups:
                #     groupobj = FunctionsGroup.query.filter_by(name=group).first()
                #     if groupobj:
                #         groupobj.functions.append(func)
                # db.session.add(groupobj)
                db.session.commit()
                return jsonify(f"function {func.name} was succefully updated")
            except Exception as error:
                # db.session.rollback()
                return jsonify(f"Not Saved! Something went wrong while saving the groups")
        except:
            return jsonify(f"unexpected error")
        finally:
            db.session.close()
    @staticmethod
    def jsonify_all():
        table = OctopusFunction.query.filter_by(project=session['current_project_id']).all()
        return jsonify([row.self_jsonify() for row in table])

    @staticmethod
    def delete_by_name(name):
        try:
            func = OctopusFunction.query.filter_by(name=name,project=session['current_project_id']).first()
            if func:
                db.session.delete(func)
                db.session.commit()
                return jsonify('Function succefully deleted')
            else:
                return jsonify('Not deleted! No function with this name')
        except:
            return jsonify('Not deleted! Something went wrong in the delete process')

    @staticmethod
    def delete_by_id(func_id):
        try:
            func = OctopusFunction.query.get(int(func_id))
            db.session.delete(func)
            db.session.commit()
            return jsonify('Function succefully deleted')
        except:
            return jsonify('Not deleted! Something went wrong in the delete process')

    @staticmethod
    def get_names():
        try:
            names = OctopusFunction.query.filter_by(project=session['current_project_id']).with_entities(OctopusFunction.name).all()
            return jsonify(status=1, message=None, data=list(*zip(*names)))
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    def get_names_json():
        try:
            function_status = ['Needed', 'InDev', 'Completed']
            functions = OctopusFunction.query.filter_by(project=session['current_project_id']).all()
            names_json = [{"name":func.name,
                           "status": function_status[func.status],
                           "owner":User.query.get(func.owner).name,
                           "feature": func.feature}
                           if func.owner
                           else
                           {"name":func.name,
                           "status": function_status[func.status],
                           "owner":"deleted user",
                           "feature": func.feature}
                           for func in functions]
            return jsonify(status=1, message=None, data=names_json)
        except:
            return jsonify(status=0, message='something went wrong', data=[])


    def run(self, db_conn, run_id, tests_params=None):
        #check if path is in os.path
        try:
            # if not self.location in sys.path:
            #     return {
            #         'run_id': run_id,
            #         'db_conn': db_conn.name,
            #         'result_status':1,
            #         'result_text':'Error! Function file is not included in Octopus Path',
            #         'result_arr' : None
            #     }

            #check if file is in path
            if not Path(self.location).exists():
                return {
                    'run_id': run_id,
                    'db_conn': db_conn.name,
                    'result_status':1,
                    'result_text':'Error! Function module is not in the specified location',
                    'results_arr' : None,
                    'time_elapsed' : 0
                }
            try:
                db_conn.connection = create_engine(db_conn.conn_string, connect_args={'connect_timeout': 5})
                conn = db_conn.connection.connect()
            except:
                try:
                    conn.close()
                    db_conn.connection.dispose()
                    db_conn.connection = None
                except:
                    db_conn.connection = None
                return {
                    'run_id': run_id,
                    'db_conn': db_conn,
                    'result_status':1,

                    'result_text':"Error! Unexpected error while connecting to db",
                    'results_arr' : None,
                    'time_elapsed' : 0
                }
            try:
                parameters_list = self.get_parameters_list(conn, run_id)
            except:

                return {
                    'run_id': run_id,
                    'db_conn': db_conn,
                    'result_status':1,
                    'result_text':"Error! Unexpected error while extracting method's parameters",
                    'results_arr' : None,
                    'time_elapsed' : 0
                }
            try:
                if self.kind.lower() == 'python':
                    #import module
                    try:
                        if self.file_name == None:
                            self.file_name = self.location.split(sep)[-1]
                            module = importlib.import_module(file_name.split('.')[-2])
                        else:
                            module = importlib.import_module(self.file_name.split('.')[-2])
                    except:
                        return {
                            'run_id': run_id,
                            'db_conn': db_conn.name,
                            'result_status':1,
                            'result_text':'Error! Error while getting the module (file)',
                            'results_arr' : None,
                            'time_elapsed' : 0
                        }
                    #if class - check for method

                    if self.is_class_method:
                        try:
                            req_class = getattr(module, self.class_name)
                            req_method = getattr(req_class, self.callback)
                        except:
                            return {
                            'run_id': run_id,
                            'db_conn': db_conn.name,
                            'result_status':1,
                            'result_text':'Error! The specified module does not contain the given class or method',
                            'results_arr' : None,
                            'time_elapsed' : 0
                            }
                    #else - check for function
                    else:
                        try:
                            req_method = getattr(module, self.callback)
                        except:
                            return {
                                'run_id': run_id,
                                'db_conn': db_conn.name,
                                'result_status':1,
                                'result_text':'Error! Unexpected error while extracting the method',
                                'results_arr' : None,
                                'time_elapsed' : 0
                            }

                        if len(parameters_list) > 0:
                            if 'Tests Params' in parameters_list:
                                index = parameters_list.index('Tests Params')
                                parameters_list[index] = tests_params
                            start_time = time()
                            result_dict = req_method(conn, run_id, *parameters_list)
                        else:
                            start_time = time()
                            result_dict = req_method(conn, run_id)
                elif self.kind.lower() == 'sql':
                    if len(parameters_list) > 0:
                        if 'Tests Params' in parameters_list:
                            index = parameters_list.index('Tests Params')
                            parameters_list[index] = tests_params
                        query = open(self.location,'r').read()
                        start_time = time()
                        result_dict = run_sql(conn, run_id, query, *parameters_list)
                    else:
                        start_time = time()
                        result_dict = run_sql(conn, run_id)

                elif self.kind.lower() == 'matlab':
                    if len(parameters_list) > 0:
                        if 'Tests Params' in parameters_list:
                            index = parameters_list.index('Tests Params')
                            parameters_list[index] = tests_params
                        start_time = time()
                        result_dict = run_matlab(conn, run_id, *parameters_list)
                    else:
                        start_time = time()
                        result_dict = run_matlab(conn, run_id)
                else:
                    return {
                        'run_id': run_id,
                        'db_conn': db_conn.name,
                        'result_status':1,
                        'result_text':'Error! Function kind must be python, sql or matlab',
                        'results_arr' : None,
                        'time_elapsed' : 0
                    }
                time_elapsed = time() - start_time
                # if str.find(str(time_elapsed),'.') > 0:
                #     str_time_elapsed = str(time_elapsed)
                #     if len(str_time_elapsed.split('.')[-1]) > 3:
                #         str_time_elapsed = str_time_elapsed.split('.')
                #         time_elapsed = float(str_time_elapsed[0]+'.'+str_time_elapsed[-1][0:3])
                conn.close()
                db_conn.connection.dispose()
                db_conn.connection = None
                result_dict['result_status'] = int(result_dict['result_status'])
                result_dict.update([('run_id', run_id), ('db_conn', db_conn.name), ('time_elapsed', time_elapsed)])
                return result_dict
            except Exception as error:
                try:
                    conn.close()
                    db_conn.connection.dispose()
                    db_conn.connection = None
                except:
                    db_conn.connection = None

                return {
                    'run_id': run_id,
                    'db_conn': db_conn.name,
                    'result_status':1,
                    'result_text':'Error! Unexpected error while activating the method',
                    'results_arr' : None,
                    'time_elapsed' : 0
                }
        except:
            return {
                'run_id': run_id,
                'db_conn': db_conn.name,
                'result_status':1,
                'result_text':'Error! Unexpected error while handling the method',
                'results_arr' : None,
                'time_elapsed' : 0
            }
        finally:
            if db_conn.connection:
                try:
                    conn.close()
                    db_conn.connection.dispose()
                    db_conn.connection = None
                except:
                    db_conn.connection = None
    # def __repr__(self):
    #     print(f'my name is {self.name} and my owner is {self.owner}')

    # def printme(self):
    #     return f'my name is {self.name} and my owner is {self.owner}'

    def get_parameters_list(self, conn, run_id):
        params_list = [param.get_value(conn, run_id) for param in self.function_parameters]
        return params_list

###############################################
########### TREES MODEL CLASS ############
###############################################


class Trees(db.Model):
    __tablename__ = "Trees"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    function = db.Column(db.Integer, db.ForeignKey('OctopusFunctions.id'))
    nodes = db.relationship(
        'TreeStructre', backref='Trees', lazy=True, uselist=True)

    def __init__(self, name=None, function=None, nodes=[]):
        self.name = name
        self.function = function
        self.nodes = nodes

    def self_jsonify(self):
        return jsonify(
            name=self.name,
            function=self.function,
            nodes=jsonify([node.self_jsonify() for node in self.nodes]).json
        ).json

    @staticmethod
    def jsonify_all():
        table = Trees.query.all()
        return jsonify([row.self_jsonify() for row in table])


##################################################
########### TREESTRUCTURE MODEL CLASS ############
##################################################

class TreeStructre(db.Model):
    __tablename__ = "TreeStructre"
    id = db.Column(db.Integer, primary_key=True)
    tree_id = db.Column(db.Integer, db.ForeignKey('Trees.id'))
    node_id = db.Column(db.Integer)
    node_name = db.Column(db.Text)
    node_data = db.Column(db.Text)
    parent = db.Column(db.Integer)

    def __init__(self, tree_id=None, node_id=None, node_name=None, node_data=None, parent=None):
        self.tree_id = tree_id
        self.node_id = node_id
        self.node_name = node_name
        self.node_data = node_data
        self.parent = parent

    def self_jsonify(self):
        return jsonify(
            tree_id=self.tree_id,
            node_id=self.node_id,
            node_name=self.node_name,
            node_data=self.node_data,
            parent=self.parent
        ).json

    @staticmethod
    def jsonify_all():
        table = TreeStructre.query.all()
        return jsonify([row.self_jsonify() for row in table])


##################################################
########### FUNCTIONSGROUP MODEL CLASS ############
##################################################

class FunctionsGroup(db.Model):
    __tablename__ = 'FunctionsGroup'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    project = db.Column(db.Integer, db.ForeignKey('Project.id'))
    functions = db.relationship('OctopusFunction', secondary=FunctionsAndGroups,
                                backref=db.backref('groups', lazy='dynamic'))
    def __init__(self, name=None, project=None, functions=[]):
        self.name = name
        self.functions = functions
        self.project = project

    def self_jsonify(self):
        return jsonify(
            id=self.id,
            name=self.name,
            functions=jsonify([func.name for func in self.functions if func.project==session['current_project_id']]).json
        ).json

    @staticmethod
    def jsonify_all():
        table = FunctionsGroup.query.filter_by(project=session['current_project_id']).all()
        return jsonify([row.self_jsonify() for row in table])

    def add_functions(self, functions_list):
        messages = []
        for index, func in enumerate(functions_list):
            #stage 1 - resolve function identifier and exracet function object
            identifier_resolved_flag=False
            if type(func) == type('1'):
                is_identifier_str_flag = True
                is_identifier_number_flag = False
                try:
                    if func.isdigit():
                        func_obj = OctopusFunction.query.get(int(func))
                        if func_obj:
                            identifier_resolved_flag=True
                        else:
                            messages.append('Error: No functions with id ' + func)
                    else:
                        func_obj = OctopusFunction.query.filter_by(name=func,project=session['current_project_id']).first()
                        if func_obj:
                            func_obj = func_obj
                            identifier_resolved_flag=True
                        else:
                            messages.append('Error: No functions with name ' + func)
                except Exception as error:
                    messages.append('Error: something went wrong while exracting the function object with' +
                                    'identifier of ' + func)
            elif type(func) == type(int(1)):
                is_identifier_str_flag = False
                is_identifier_number_flag = True
                try:
                    func_obj = OctopusFunction.query.get(func)
                    if func_obj:
                        identifier_resolved_flag=True
                    else:
                        messages.append('Error: No functions with id ' + func)
                except Exception as error:
                    messages.append('Error: something went wrong while exracting the function object with' +
                                    'identifier of ' + str(func))
            else:
                messages.append('Error: unsupported function identifier in the ' + str(index) + 'th place. identifier must be id or name')

            #stage 2 - append the functions to the group
            if identifier_resolved_flag:
                identifier_resolved_flag=False
                try:
                    self.functions.append(func_obj)
                except:
                    if is_identifier_str_flag:
                        messages.append('Error: something went wrong while adding the function with id or name ' + func)
                    if is_identifier_number_flag:
                        messages.append('Error: something went wrong while adding the function with id ' + func)
        #stage 3 - commit changes to db and return the messages
        db.session.commit()
        return messages
    @staticmethod
    def save(json_data):
        try:
            messages = []
            name = json_data['name']
            if name in [group.name for group in FunctionsGroup.query.filter_by(project=session['current_project_id']).all()]:
                return jsonify(status=0, message=['cannot create - group with this name already exist'], data=None)
            group = FunctionsGroup(name=name, project=session['current_project_id'])
            db.session.add(group)
            db.session.commit()
            functions = json_data['functions']
            status=0
            if functions:
                if type(functions) == type([1]):
                    messages = group.add_functions(functions)
                    if not messages:
                        status=1
                else:
                    messages.append('Error: functions identifiers must be contained in an array')
            else:
                status=1
            return jsonify(status=status, message=messages, data=None)
        except Exception as error:
            messages = messages.append('something went wrong in the saving process')
            return jsonify(status=0, message=messages, data=None)
        finally:
            db.session.close()

    @staticmethod
    def get_names():
        try:
            names = FunctionsGroup.query.filter_by(project=session['current_project_id']).with_entities(FunctionsGroup.name).all()
            return jsonify(status=1, message=None, data=list(*zip(*names)))
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def get_names_json():
        try:
            names = FunctionsGroup.query.filter_by(project=session['current_project_id']).with_entities(FunctionsGroup.name).all()
            names_json = [{"name":name} for name in names]
            return jsonify(status=1, message=None, data=names_json)
        except:
            return jsonify(status=0, message='something went wrong', data=[])
        finally:
            db.session.close()

    @staticmethod
    def get_by_id(group_id):
        try:
            group = FunctionsGroup.query.get(int(group_id))
            return jsonify(status=1, message=None, data=group.self_jsonify())
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def get_by_name(group_name):
        try:
            group = FunctionsGroup.query.filter_by(name=group_name,project=session['current_project_id']).first()
            return jsonify(status=1, message=None, data=group.self_jsonify())
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def get_num_of_functions_by_name(group_name):
        try:
            group = FunctionsGroup.query.filter_by(name=group_name,project=session['current_project_id']).first()
            return jsonify(status=1, message=None, data=len(group.functions))
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def delete_by_name(name):
        try:
            group = FunctionsGroup.query.filter_by(name=name, project=session['current_project_id']).first()
            if group:
                db.session.delete(group)
                db.session.commit()
                return jsonify(status=1,message='group ' + name + ' succefully deleted')
            else:
                return jsonify(status=0,message='Not deleted! No group with this name')
        except:
            return jsonify(status=0,message='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def delete_by_id(group_id):
        try:
            group = FunctionsGroup.query.get(int(group_id))
            if group:
                db.session.delete(group)
                db.session.commit()
                return jsonify(status=1,message='group ' + group.name + ' succefully deleted')
            else:
                return jsonify(status=0,message='Not deleted! No group with this id')
        except:
            return jsonify(status=0,message='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def update_by_name(name, json_data):
        try:
            group = FunctionsGroup.query.filter_by(name=name,project=session['current_project_id']).first()
            if group:
                updated_functions = json_data['functions']
                if not type(updated_functions) == type([1]):
                    return jsonify(status=1,message='not updated! functions must be sent as an array/list')
                group.functions = []
                messages = group.add_functions(updated_functions)
                # group.name = json_data['name']

                db.session.add(group)
                db.session.commit()
                if messages:
                    return jsonify(status=0,message=messages)
                else:
                    return jsonify(status=1,message='group ' + group.name + ' succesfully updated')
            else:
                return jsonify(status=0,message='Not deleted! No group with this name')


            return jsonify(status= 1, message='group '  + group.name + ' succesfully updated')
        except Exception as error:
            return jsonify(status=0, message='Not updated! something went wrong - please try again later')
        finally:
            db.session.close()

    def get_functions_ids(self):
        if self.functions:
            return [func.id for func in self.functions]
        return None

    @staticmethod
    def update_by_id(group_id, json_data):
        try:
            group = FunctionsGroup.query.get(int(group_id))
            if group:
                updated_functions = json_data['functions']
                if not type(updated_functions) == type([1]):
                    return jsonify(status=1,message='not updated! functions must be sent as an array/list')
                group.functions = []
                messages = group.add_functions(updated_functions)
                # group.name = json_data['name']

                db.session.add(group)
                db.session.commit()
                if messages:
                    return jsonify(status=0,message=messages)
                else:
                    return jsonify(status=1,message='group ' + group.name + ' succesfully updated')
            else:
                return jsonify(status=0,message='Not deleted! No group with this name')
            return jsonify(status= 1, message='group '  + group.name + ' succesfully updated')
        except Exception as error:
            return jsonify(status=0, message='Not updated! something went wrong - please try again later')
        finally:
            db.session.close()
##################################################
########### DBCONNECTION MODEL CLASS #############
##################################################

class DbConnections(db.Model):
    __tablename__ = 'DbConnections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    db_type = db.Column(db.Text)
    user = db.Column(db.Text)
    password = db.Column(db.Text)
    hostname = db.Column(db.Text)
    port = db.Column(db.Text)
    schema = db.Column(db.Text)
    conn_string = db.Column(db.Text)
    project = db.Column(db.Integer, db.ForeignKey('Project.id'))

    def __init__(self, db_type, user, password, hostname, port, schema, name, conn_string, project=None):
        self.db_type = db_type
        self.schema = schema
        self.user = user
        self.password = password
        self.hostname = hostname
        self.port = port
        self.name = name
        self.conn_string = conn_string
        self.project = project

    def self_jsonify(self):
        return jsonify(
            db_type = self.db_type,
            schema = self.schema,
            user = self.user,
            password = self.password,
            hostname = self.hostname,
            port = self.port,
            name = self.name,
            conn_string = self.conn_string
        ).json

    @staticmethod
    def get_names():
        connections = DbConnections.query.filter_by(project=session['current_project_id']).all()
        return jsonify([conn.name for conn in connections])
##################################################
########### ERRORLOG MODEL CLASS ####################
##################################################
class ErrorLog(db.Model):
    __tablename__ = 'ErrorLog'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer)
    error_time = db.Column(db.DateTime)
    stage = db.Column(db.Text)
    error_string = db.Column(db.Text)

    def __init__(self, error_string, error_time=datetime.utcnow(), task_id=None,stage='unknown'):
        self.task_id = task_id
        self.error_time = error_time
        self.stage = stage
        self.error_string = error_string

    def log(self):
        db.session.add(self)
        db.session.commit()

    def push(self, error_queue):
        error_queue.put_nowait(self)

class AnalyseTask(db.Model):
    __tablename__ = "AnalyseTask"
    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer)
    mission_type = db.Column(db.Integer)
    function_id = db.Column(db.Integer)
    run_id = db.Column(db.Integer)
    run_status = db.Column(db.Integer)
    scenario_name = db.Column(db.Text)
    scenario_id = db.Column(db.Integer)
    ovr_file_location = db.Column(db.Text)
    db_conn_string = db.Column(db.Text)
    priority = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    message = db.Column(db.Text)
    time_elapsed = db.Column(db.Float)

    def __init__(self, mission_id=None, mission_type=0, function_id=None,
                 run_id=None, run_status=None,scenario_name=None ,scenario_id=None, ovr_file_location=None, db_conn_string=None,
                 priority=1, user_id=None, status=-3, message=None,time_elapsed=0):

        self.mission_id = mission_id
        self.mission_type = mission_type
        self.function_id = function_id
        self.run_id = run_id
        self.run_status = run_status
        self.scenario_name = scenario_name
        self.scenario_id = scenario_id
        self.ovr_file_location = ovr_file_location
        self.db_conn_string = db_conn_string
        self.priority = priority
        self.user_id = user_id
        self.status = status
        self.message = message
        self.time_elapsed = time_elapsed

        #status
        #0 - created
        #1 - failure pushing to tasks queue
        #2 - in tasks_queue
        #3 - faiiure running task
        #4 - task done. waiting to be written to db
        #5 - failure writing to db
        #6 - results in db

    def push(self):

        global tasks_queue
        tasks_queue.put_nowait((self, OctopusFunction.query.get(self.function_id), datetime.utcnow(), self.id))

    @staticmethod
    def get_mission_results(mission_identifier):
        statistics = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if type(mission_identifier) == type("1"):
            if mission_identifier.isdigit():
                mission_id = int(mission_identifier)
            else:
                mission_id = mission_identifier.split('_')[-1]
        else:
            mission_id = mission_identifier
        tasks = AnalyseTask.query.filter_by(mission_id=mission_id).all()
        for task in tasks:
            statistics[task.status]+=1
        is_done = True
        if [True for task in tasks if task.status == -3]:
            is_done = False
        table_columns = list(set([task.db_conn_string + '-' + str(task.run_id) + '-' + task.scenario_name
                   for task in tasks]))
        table_columns = ["function name","function state","requirement","owner"] + table_columns
        table_columns = [{ "title": col, "data": col } for col in table_columns]
        functions_ids = list(set([tasks.function_id for tasks in tasks]))
        functions_dict = {}
        [functions_dict.update({func_id:None}) for func_id in functions_ids]
        functions = db.session.query(OctopusFunction).filter(OctopusFunction.id.in_(functions_ids)).all()
        [functions_dict.update({func.id:{
                                        "function name":func.name,
                                        "function state" : func.status,
                                        "requirement": func.requirement,
                                        "owner" : User.query.get(func.owner).name
                                        }})
         if func.owner else 
         functions_dict.update({func.id:{
                                        "function name":func.name,
                                        "function state" : func.status,
                                        "requirement": func.requirement,
                                        "owner" : 'deleted user'
                                        }})                               
                                        for func in functions]
        [functions_dict[task.function_id].update({
            task.db_conn_string + '-' + str(task.run_id) + '-' + task.scenario_name: task.status
        }) for task in tasks]
        report = {"table_data":[functions_dict[key] for key in functions_dict.keys()],
                  "table_columns": table_columns,
                  "is_done":is_done, "statistics":statistics
                  }
        return jsonify(status = 1, message=None, data=report)
class Mission(db.Model):
    __tablename__ = 'Mission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    project = db.Column(db.Integer)
    def __init__(self, name=None, project=None):
        if name:
            self.name=name
        else:
            self.name='mission'+str(self.id)
        self.project = project

    # @staticmethod
    # def push_task(user_id, function, run_id, db_conn)

    @staticmethod
    def create_mission(json_data,tasks_queue):
        # global tasks_queue
        if not type(json_data['functions']) == type(list()):
            json_data['functions'] = [json_data['functions']]
        functions = db.session.query(OctopusFunction).filter(OctopusFunction.id.in_( json_data['functions'])).all()
        names = [func.name for func in functions]
        runs = json_data['runs']

        mission = Mission(json_data['mission_name'], project=session['current_project_id'])
        db.session.add(mission)
        db.session.commit()
        user_id = json_data['user_id']
        for db_name in runs:
            conn = DbConnector.load_conn_by_name(db_name)
            run_ids = [run for run in runs[db_name]]
            if not type(run_ids) == type(list()):
                run_ids = run_ids
            for run in run_ids:
                for func in functions:
                    task = Task(mission.id, conn, run, func.id, user_id)
                    tasks_queue.put_nowait(task)

        return str(mission.id)

    def self_jsonify(self):
        return jsonify(
            id=self.id,
            name = self.name).json


    @staticmethod
    def jsonify_all():
        table = Mission.query.all()
        return jsonify([row.self_jsonify() for row in table])

    @staticmethod
    def get_ids():
        table = Mission.query.all()
        ids = [row.id for row in table]
        ids.sort(reverse=True)
        return jsonify(ids)

    @staticmethod
    def get_names():
        table = Mission.query.all()
        names = [row.name for row in table]
        ids_dict = {}
        ids = [row.id for row in table]
        ids.sort(reverse=True)
        [ids_dict.update({row.id:row.name}) for row in table]
        names = [ids_dict[index] for index in ids]
        return jsonify(names)
class OverView(db.Model):
    __tablename__ = 'OverView'
    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer)
    overall_status = db.Column(db.Integer)
    # result_id = db.relationship('AnalyseResult', backref='OverView', lazy=True, uselist=True)
    elapsed_time = db.Column(db.Float)

    # def __init__(self, mission_id, results, overall_status=None, result_id=[] , time_elapsed=None):
    #     self.mission_id = mission_id
    #     self.overall_status = overall_status
    #     # self.result_id = result_id
    #     self.time_elapsed = time_elapsed
    #     db.session.add(self)
    #     db.session.commit()
    #     for result in results:
    #         analyse_result = AnalyseResult(overview_id=self.id, run_id=result['run_id'], db_conn='db_conn',
    #                                        result_status=result['result_status'],
    #                                        result_text=result['result_text'],
    #                                        result_array=result['results_arr'])#,
                                        #    result_array_header=[],#result['result_array_header'],
                                        #    result_array_types=[])#=result['result_array_types'])




class AnalyseResult(db.Model):
    __tablename__ = 'AnalyseResult'
    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer)
    # overview_id = db.Column(db.Integer, db.ForeignKey('OverView.id'))
    task_id = db.Column(db.Integer)
    run_id = db.Column(db.Integer)
    scenario_name = db.Column(db.Text)
    run_status = db.Column(db.Integer)
    function_id = db.Column(db.Integer)
    db_conn = db.Column(db.Text)
    result_status = db.Column(db.Integer)
    result_text = db.Column(db.Text)
    result_array = db.relationship('ResultArray', backref='AnalyseResult', lazy=True, uselist=True)
    result_array_header = db.Column(db.Text)
    result_array_types = db.Column(db.Text)
    time_elapsed = db.Column(db.Float)

    def __init__(self, mission_id, task_id, run_id,scenario_name, run_status, function_id, result_status, result_text,
                db_conn_string=None, result_array=None, result_array_header=None, result_array_types=None, time_elapsed=None):
        self.mission_id = mission_id
        self.task_id = task_id
        self.run_id = run_id
        self.scenario_name = scenario_name
        self.run_status = run_status
        self.function_id = function_id
        self.db_conn = db_conn_string
        self.result_status = result_status
        self.result_text = result_text
        self.result_array = []
        self.result_array_types = result_array_types
        self.time_elapsed = time_elapsed
        # db.session.add(self)
        # db.session.commit()

    @staticmethod
    def extract_headers(data_obj):
        status = False
        message = ''
        header = None
        if type(data_obj) == type(pd.DataFrame()):
            cols = list(data_obj.columns)
            if not len(cols) > 30:
                header = ','.join(cols)
                # for col in cols:
                #     header += col
                status = True
            else:
                message = 'result array must not have more than 30 columns'
        else:
            message = 'result array must be a DataFrame'

        return (status, message, header)

    def log(self, data_obj, error_queue):
        db.session.add(self)
        self.time_elapsed = float(self.time_elapsed)
        db.session.commit()
        message = ''
        try:
            status, message, self.result_array_header = AnalyseResult.extract_headers(data_obj)
            if status:
                if len(data_obj.index)>0:
                    data_obj = data_obj.astype(str)
                    for index, row in data_obj.iterrows():
                        result_array = ResultArray(self.id, *list(row.values))
                        db.session.add(result_array)
                        db.session.commit()
                else:
                    message = 'Return None for no result array and not an empty DataFrame'
                    error_log = ErrorLog(task_id = self.task_id, stage='logging result array', error_string=message)
                    error_log.push(error_queue)
            else:
                error_log = ErrorLog(task_id = self.task_id, stage='logging result array', error_string=message)
                error_log.push(error_queue)
        except:
            message = 'something went wrong while logging the result array'
            error_log = ErrorLog(task_id = self.task_id, stage='logging result array', error_string=message)
            error_log.push(error_queue)

        db.session.add(self)
        db.session.commit()
        return message

    def self_jsonify(self):
        if self.result_array_header:
            result_array = self.tablify_results_arrays()
        else:
            result_array = None

        function_obj = OctopusFunction.query.get(self.function_id)
        if function_obj:
            function_id = function_obj.id
            function_status = function_obj.status
            user = User.query.get(OctopusFunction.query.get(function_id).owner)
            if user:
                user_name = user.name
            else:
                user_name = None
        else:
            function_id = None
            user_name=None

        return jsonify(
            id=self.id,
            task_id = self.task_id,
            function_id = function_id,
            run_id = self.run_id,
            db_conn = self.db_conn,
            result_status = self.result_status,
            result_text = self.result_text,
            result_array_types = self.result_array_types,
            result_array=result_array,
            function_state = function_status,
            function_owner = user_name
        )

    def tablify_results_arrays(self):
        res_arr = pd.DataFrame([{col:val for col, val in result.self_jsonify().items() if val}
                    for result in self.result_array])
        column_names = {'col'+str(num+1):header
                        for num, header in enumerate(self.result_array_header.split(','))}
        res_arr = res_arr.rename(columns=column_names)
        return jsonify(json.loads(res_arr.to_json(orient='table'))).json

    @staticmethod
    def jsonify_by_ids(*args):
        # if not type(ids) == type([1]):
        ids = list(args)
        ids = [int(id) for id in ids]
        results = db.session.query(AnalyseResult).filter(AnalyseResult.id.in_(ids)).all()
        return jsonify([result.self_jsonify().json for result in results])

    @staticmethod
    def get_by_mission_id(mission_id):
        results = AnalyseResult.query.filter_by(mission_id = mission_id).all()
        if results:
            return jsonify(status=1, data=[result.id for result in results],message=None)
        else:
            return jsonify(status=0, data=None,message=['no results for this mission id'])

    @staticmethod
    def get_by_mission_name(mission_name):
        mission = Mission.query.filter_by(name=mission_name,project=session['current_project_id']).first()
        if mission:
            mission_id = mission.id
        else:
            return jsonify(status=0, data=None,message=['no mission with this name'])

        results = AnalyseResult.query.filter_by(mission_id = mission_id).with_entities('AnalyseResult.id').all()
        
        if results:
            return jsonify(status=1, data=[result.id for result in results],message=None)
        else:
            return jsonify(status=0, data=None,message=['no results for this mission id'])


    @staticmethod
    def jsonify_by_mission_id(id):
        tasks = AnalyseTask.query.filter_by(mission_id=int(id)).all()
        # mission_results = [{'task_status':task.status,'run_id':task.run_id,
        #             'function_name':OctopusFunction.query.get(task.function_id).name,
        #             'status:':AnalyseResult.query.filter_by(task_id=task.id)[0].result_status}
        #             for task in tasks]
        # functions = list(set([OctopusFunction.query.get(task.function_id).name for task in tasks]))
        # run_ids = list(set([task.run_id for task in tasks]))
        # ids = [int(task.id) for task in tasks]
        # ids = db.session.query(AnalyseResult).filter(AnalyseResult.task_id.in_(ids)).with_entities(AnalyseResult.id).all()
        # # ids = list(zip(*ids))
        # data = AnalyseResult.jsonify_by_ids(*list((*zip(*ids)))).json
        mission_results = [{'function_name':OctopusFunction.query.get(task.function_id).name,
                            'function_state':OctopusFunction.query.get(task.function_id).status,
                            'requirement':OctopusFunction.query.get(task.function_id).requirement,
                            'owner' : User.query.get(OctopusFunction.query.get(task.function_id).owner).name,
                            task.db_conn_string+ ' - ' +str(task.run_id):{
                                            'result_id':AnalyseResult.query.filter_by(task_id=task.id)[0].id,
                                            'status':AnalyseResult.query.filter_by(task_id=task.id)[0].result_status,
                                            'time_elapsed' : AnalyseResult.query.filter_by(task_id=task.id)[0].time_elapsed
                                        }
                            }

                            if task.status == 4
                            else
                            {'function_name':OctopusFunction.query.get(task.function_id).name,
                            'function_state':OctopusFunction.query.get(task.function_id).status,
                            'requirement':OctopusFunction.query.get(task.function_id).requirement,
                            'owner' : User.query.get(OctopusFunction.query.get(task.function_id).owner).name,
                            task.db_conn_string+ ' - ' +str(task.run_id):-1}
                            for task in tasks]
        res_df = pd.DataFrame(mission_results)
        if res_df.empty:
            return jsonify(None)
        res_df = res_df.set_index('function_name').groupby(level=0).last()
        return jsonify(json.loads(res_df.to_json(orient='table')))
        # return jsonify(data=mission_results, run_ids = run_ids, functions=functions)

class ResultArray(db.Model):
    __tablename__ = 'ResultArray'
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('AnalyseResult.id'))
    col1 = db.Column(db.Text)
    col2 = db.Column(db.Text)
    col3 = db.Column(db.Text)
    col4 = db.Column(db.Text)
    col5 = db.Column(db.Text)
    col6 = db.Column(db.Text)
    col7 = db.Column(db.Text)
    col8 = db.Column(db.Text)
    col9 = db.Column(db.Text)
    col10 = db.Column(db.Text)
    col11 = db.Column(db.Text)
    col12 = db.Column(db.Text)
    col13 = db.Column(db.Text)
    col14 = db.Column(db.Text)
    col15 = db.Column(db.Text)
    col16 = db.Column(db.Text)
    col17 = db.Column(db.Text)
    col18 = db.Column(db.Text)
    col19 = db.Column(db.Text)
    col20 = db.Column(db.Text)
    col21 = db.Column(db.Text)
    col22 = db.Column(db.Text)
    col23 = db.Column(db.Text)
    col24 = db.Column(db.Text)
    col25 = db.Column(db.Text)
    col26 = db.Column(db.Text)
    col27 = db.Column(db.Text)
    col28 = db.Column(db.Text)
    col29 = db.Column(db.Text)
    col30 = db.Column(db.Text)

    def __init__(self, result_id, col1,
                col2 = None,
                col3 = None,
                col4 = None,
                col5 = None,
                col6 = None,
                col7 = None,
                col8 = None,
                col9 = None,
                col10 = None,
                col11 = None,
                col12 = None,
                col13 = None,
                col14 = None,
                col15 = None,
                col16 = None,
                col17 = None,
                col18 = None,
                col19 = None,
                col20 = None,
                col21 = None,
                col22 = None,
                col23 = None,
                col24 = None,
                col25 = None,
                col26 = None,
                col27 = None,
                col28 = None,
                col29 = None,
                col30 = None
                ):
        self.result_id = result_id
        self.col1 = col1
        self.col2 = col2
        self.col3 = col3
        self.col4 = col4
        self.col5 = col5
        self.col6 = col6
        self.col7 = col7
        self.col8 = col8
        self.col9 = col9
        self.col10 = col10
        self.col11 = col11
        self.col12 = col12
        self.col13 = col13
        self.col14 = col14
        self.col15 = col15
        self.col16 = col16
        self.col17 = col17
        self.col18 = col18
        self.col19 = col19
        self.col20 = col20
        self.col21 = col21
        self.col22 = col22
        self.col23 = col23
        self.col24 = col24
        self.col25 = col25
        self.col26 = col26
        self.col27 = col27
        self.col28 = col28
        self.col29 = col29
        self.col30 = col30

    def self_jsonify(self):

        return jsonify(
            result_id = self.result_id,
            col1 = self.col1,
            col2 = self.col2,
            col3 = self.col3,
            col4 = self.col4,
            col5 = self.col5,
            col6 = self.col6,
            col7 = self.col7,
            col8 = self.col8,
            col9 = self.col9,
            col10 =self.col10,
            col11 =self.col11,
            col12 =self.col12,
            col13 =self.col13,
            col14 =self.col14,
            col15 =self.col15,
            col16 =self.col16,
            col17 =self.col17,
            col18 =self.col18,
            col19 =self.col19,
            col20 =self.col20,
            col21 =self.col21,
            col22 =self.col22,
            col23 =self.col23,
            col24 =self.col24,
            col25 =self.col25,
            col26 =self.col26,
            col27 =self.col27,
            col28 =self.col28,
            col29 =self.col29,
            col30 =self.col30
        ).json


class Site(db.Model):
    __tablename__ = 'site'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Project.id'))
    name = db.Column(db.Text)
    version = db.Column(db.Text)
    is_active = db.Column(db.Integer)
    site_ip = db.Column(db.Text)
    recording_db_ip = db.Column(db.Text)
    execrsice_site_ip = db.Column(db.Text)
    execrsice_db_ip = db.Column(db.Text)
    auto_data_site_ip = db.Column(db.Text)
    auto_data_db_ip = db.Column(db.Text)
    nets =db.Column(db.Text)
    stations = db.Column(db.Text)
    changed_date = db.Column(db.DateTime)
    # port = db.Column(db.Integer) new
    # service_name = db.Column(db.Text) new
    changed_by = db.Column(db.Integer)

    def __init__(self, project_id, name, version, is_active, site_ip, recording_db_ip,
                 execrsice_site_ip, execrsice_db_ip, auto_data_site_ip,
                 auto_data_db_ip, nets, stations, changed_by):
        self.project_id = project_id
        self.name = name
        self.version = version
        self.is_active = is_active
        self.site_ip = site_ip
        self.recording_db_ip = recording_db_ip
        self.execrsice_site_ip = execrsice_site_ip
        self.execrsice_db_ip = execrsice_db_ip
        self.auto_data_site_ip = auto_data_site_ip
        self.auto_data_db_ip = auto_data_db_ip
        self.nets = nets
        self.stations = stations
        self.changed_date = datetime.utcnow()
        self.changed_by = changed_by

    def self_jsonify(self):
        if self.changed_by:
            user = User.query.get(self.changed_by)
            if user:
                user_name = user.name
            else:
                user_name = None
        else:
            user_name = None
        return jsonify(
                project_id = self.project_id,
                name = self.name,
                version = self.version,
                is_active = self.is_active,
                site_ip = self.site_ip,
                recording_db_ip = self.recording_db_ip,
                execrsice_site_ip = self.execrsice_site_ip,
                execrsice_db_ip = self.execrsice_db_ip,
                auto_data_site_ip = self.auto_data_site_ip,
                auto_data_db_ip = self.auto_data_db_ip,
                nets = self.nets,
                stations = self.stations,
                changed_date = self.changed_date,
                changed_by = user_name
            ).json

    @staticmethod
    def get_names():
        try:
            names = Site.query.with_entities(Site.name).all()
            return jsonify(status=1, message=None, data=list(*zip(*names)))
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()


    def get_names_by_project_name(project_name):
        try:
            project_id = Project.query.filter_by(name=project_name).first().id
            names = Site.query.filter_by(project_id=project_id).with_entities(Site.name).all()
            return jsonify(status=1, message=None, data=list(*zip(*names)))
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def get_by_id(site_id):
        try:
            site = Site.query.get(int(site_id))
            return jsonify(status=1, message=None, data=site.self_jsonify())
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def get_by_name(site_name):
        try:
            site = Site.query.filter_by(name=site_name).first()
            return jsonify(status=1, message=None, data=site.self_jsonify())
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def save(json_data):
        try:
            if json_data['name'] in [site.name for site in Site.query.all()]:
                return jsonify(status=0, message='Not saved! a site with this name already exist')
            project_id = Project.query.filter_by(name=json_data['project_name']).first().id
            name = json_data['name']
            version = json_data['version']
            is_active = json_data['is_active']
            site_ip = json_data['site_ip']
            recording_db_ip = json_data['recording_db_ip']
            execrsice_site_ip = json_data['execrsice_site_ip']
            execrsice_db_ip = json_data['execrsice_db_ip']
            auto_data_site_ip = json_data['auto_data_site_ip']
            auto_data_db_ip = json_data['auto_data_db_ip']
            nets = json_data['nets']
            stations = json_data['stations']
            changed_date = datetime.utcnow()
            changed_by = User.query.filter_by(name=session['username']).first().id

            site = Site(project_id, name, version, is_active, site_ip, recording_db_ip,
                    execrsice_site_ip, execrsice_db_ip, auto_data_site_ip,
                    auto_data_db_ip, nets, stations, changed_by)

            db.session.add(site)
            db.session.commit()

            return jsonify(status= 1, message='site '  + site.name + ' succesfully saved')
        except Exception as error:
            return jsonify(status=0, message='Not saved! something went wrong - please try again later')
        finally:
            db.session.close()

    @staticmethod
    def delete_by_name(name):
        try:
            site = Site.query.filter_by(name=name).first()
            if site:
                db.session.delete(site)
                db.session.commit()
                return jsonify(status=1,message='site ' + name + ' succefully deleted')
            else:
                return jsonify(status=0,message='Not deleted! No site with this name')
        except:
            return jsonify(status=0,message='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def delete_by_id(site_id):
        try:
            site = Site.query.get(int(site_id))
            if site:
                db.session.delete(site)
                db.session.commit()
                return jsonify(status=1,message='site ' + name + ' succefully deleted')
            else:
                return jsonify(status=0,message='Not deleted! No site with this id')
        except:
            return jsonify(status=0,message='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def update_by_name(name, json_data):
        try:
            site = Site.query.filter_by(name=name).first()
            if site:
                site.project_id = Project.query.filter_by(name=json_data['project_name']).first().id
                site.name = json_data['name']
                site.version = json_data['version']
                site.is_active = json_data['is_active']
                site.site_ip = json_data['site_ip']
                site.recording_db_ip = json_data['recording_db_ip']
                site.execrsice_site_ip = json_data['execrsice_site_ip']
                site.execrsice_db_ip = json_data['execrsice_db_ip']
                site.auto_data_site_ip = json_data['auto_data_site_ip']
                site.auto_data_db_ip = json_data['auto_data_db_ip']
                site.nets = json_data['nets']
                site.stations = json_data['stations']
                site.changed_date = datetime.utcnow()

                user_id = User.query.filter_by(name=session['username']).first().id
                if user_id:
                    site.changed_by = user_id
                else:
                    return jsonify(status=0,message='Not updated! No user with given name')
                db.session.add(site)
                db.session.commit()
                return jsonify(status=1,message='site ' + site.name + ' succesfully updated')
            else:
                return jsonify(status=0,message='Not deleted! No site with this name')


            return jsonify(status= 1, message='site '  + site.name + ' succesfully updated')
        except Exception as error:
            return jsonify(status=0, message='Not updated! something went wrong - please try again later')
        finally:
            db.session.close()

    @staticmethod
    def update_by_id(site_id, json_data):
        try:
            site = Site.query.get(int(site_id))
            if site:
                site.project_id = json_data['project_id']
                site.name = json_data['name']
                site.version = json_data['version']
                site.is_active = json_data['is_active']
                site.site_ip = json_data['site_ip']
                site.recording_db_ip = json_data['recording_db_ip']
                site.execrsice_site_ip = json_data['execrsice_site_ip']
                site.execrsice_db_ip = json_data['execrsice_db_ip']
                site.auto_data_site_ip = json_data['auto_data_site_ip']
                site.auto_data_db_ip = json_data['auto_data_db_ip']
                site.nets = json_data['nets']
                site.stations = json_data['stations']
                site.changed_date = datetime.utcnow()

                user_id = User.query.filter_by(name=json_data['changed_by']).first().id
                if user_id:
                    site.changed_by = user_id
                else:
                    return jsonify(status=0,message='Not updated! No user with given name')
                db.session.add(site)
                db.session.commit()
                return jsonify(status=1,message='site ' + site.name + ' succefully updated')
            else:
                return jsonify(status=0,message='Not deleted! No site with this name')
            return jsonify(status= 1, message='site '  + site.name + ' succesfully updated')
        except Exception as error:
            return jsonify(status=0, message='Not updated! something went wrong - please try again later')
        finally:
            db.session.close()

class OctopusProcess(db.Model):
    __tablename__ = 'OctopusProcess'
    id = db.Column(db.Integer, primary_key=True)
    # project_id = db.Column(db.Integer, db.ForeignKey('Project.id'))
    name = db.Column(db.Text)
    owner_id = db.Column(db.Integer)
    tags = db.Column(db.Text)
    description = db.Column(db.Text)
    stage_id = db.Column(db.Integer)
    stage_type = db.Column(db.Text)
    order = db.Column(db.Integer)
    changed_date = db.Column(db.DateTime)

    def __init__(self,name, owner_id, tags, description, stage_id, stage_type, order):
        self.name = name
        self.owner_id = owner_id
        self.tags = tags
        self.description = description
        self.stage_id = stage_id
        self.stage_type = stage_type
        self.order = order
        self.changed_date = datetime.utcnow()

    def self_jsonify(self):

        return jsonify(
                name = self.name,
                owner_id = self.owner_id,
                tags = self.tags,
                description = self.description,
                stage_id = self.stage_id,
                stage_type = self.stage_type,
                order = self.order,
                changed_date = self.changed_date
            ).json

    @staticmethod
    def get_names():
        try:
            names = OctopusProcess.query.with_entities(OctopusProcess.name).all()
            return jsonify(status=1, message=None, data=list(*zip(*names)))
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def get_by_id(process_id):
        try:
            process = OctopusProcess.query.get(int(process_id))
            return jsonify(status=1, message=None, data=process.self_jsonify())
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def get_by_name(process_name):
        try:
            process = OctopusProcess.query.filter_by(name=process_name).first()
            return jsonify(status=1, message=None, data=process.self_jsonify())
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()


    @staticmethod
    def save(json_data):
        try:
            if json_data['name'] in [process.name for process in OctopusProcess.query.all()]:
                return jsonify(status=0, message='Not saved! a process_name with this name already exist')
            name = json_data['name']
            owner_id = int(json_data['owner_id']),
            tags = json_data['tags'],
            description = json_data['description'],
            stage_id = int(json_data['stage_id']),
            stage_type = json_data['stage_type'],
            order = int(json_data['order']),
            changed_date = datetime.utcnow()



            process = OctopusProcess(name, owner_id, tags, description, stage_id, stage_type, order)

            db.session.add(process)
            db.session.commit()

            return jsonify(status= 1, message='process '  + process.name + ' succesfully saved')
        except Exception as error:
            return jsonify(status=0, message='Not saved! something went wrong - please try again later')
        finally:
            db.session.close()

    @staticmethod
    def delete_by_name(name):
        try:
            process = OctopusProcess.query.filter_by(name=name).first()
            if process:
                db.session.delete(process)
                db.session.commit()
                return jsonify(status=1,message='process ' + name + ' succefully deleted')
            else:
                return jsonify(status=0,message='Not deleted! No process with this name')
        except:
            return jsonify(status=0,message='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def delete_by_id(process_id):
        try:
            process = OctopusProcess.query.get(int(process_id))
            if process:
                db.session.delete(process)
                db.session.commit()
                return jsonify(status=1,message='process ' + name + ' succefully deleted')
            else:
                return jsonify(status=0,message='Not deleted! No process with this id')
        except:
            return jsonify(status=0,message='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def update_by_name(name, json_data):
        try:
            process = OctopusProcess.query.filter_by(name=name).first()
            if process:
                process.name = json_data['name']
                process.owner_id = int(json_data['owner_id']),
                process.tags = json_data['tags'],
                process.description = json_data['description'],
                process.stage_id = int(json_data['stage_id']),
                process.stage_type = json_data['stage_type'],
                process.order = int(json_data['order']),
                process.changed_date = datetime.utcnow()

                owner_id = User.query.get(int(process.owner_id)).id
                if owner_id:
                    process.changed_by = owner_id
                else:
                    return jsonify(status=0,message='Not updated! No user with given name')
                db.session.add(process)
                db.session.commit()
                return jsonify(status=1,message='process ' + process.name + ' succesfully updated')
            else:
                return jsonify(status=0,message='Not deleted! No process with this name')


            return jsonify(status= 1, message='process '  + process.name + ' succesfully updated')
        except Exception as error:
            return jsonify(status=0, message='Not updated! something went wrong - please try again later')
        finally:
            db.session.close()

    @staticmethod
    def update_by_id(process_id, json_data):
        try:
            process = OctopusProcess.query.get(int(process_id))
            if process:
                process.name = json_data['name']
                process.owner_id = int(json_data['owner_id']),
                process.tags = json_data['tags'],
                process.description = json_data['description'],
                process.stage_id = int(json_data['stage_id']),
                process.stage_type = json_data['stage_type'],
                process.order = int(json_data['order']),
                process.changed_date = datetime.utcnow()

                owner_id = User.query.get(int(process.owner_id)).id
                if owner_id:
                    process.changed_by = owner_id
                else:
                    return jsonify(status=0,msg='Not updated! No user with given name')
                db.session.add(process)
                db.session.commit()
                return jsonify(status=1,msg='process ' + process.name + ' succesfully updated')
            else:
                return jsonify(status=0,msg='Not deleted! No process with this name')


            return jsonify(status= 1, message='process '  + process.name + ' succesfully updated')
        except Exception as error:
            return jsonify(status=0, message='Not updated! something went wrong - please try again later')
        finally:
            db.session.close()

class ComplexNet(db.Model):
    __tablename__ = 'ComplexNet'
    id = db.Column(db.Integer, primary_key=True)
    Project_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    owner_id = db.Column(db.Integer)
    tags = db.Column(db.Text)
    description = db.Column(db.Text)
    config_id = db.relationship('NetConfig', backref='ComplexNet', lazy=True, uselist=False)
    systems_id = db.relationship('NetSystem', backref='ComplexNet', lazy=True, uselist=False)
    changed_date = db.Column(db.DateTime)

    def __init__(self,name, owner_id, tags, description, config_id=None, systems_id=None):
        self.name = name
        self.owner_id = owner_id
        self.tags = tags
        self.description = description
        self.config_id = config_id
        self.systems_id = systems_id
        self.changed_date = datetime.utcnow()

    def self_jsonify(self):
        if self.config_id:
            config_data = self.config_id.self_jsonify()
        else:
            config_data = None
        if self.systems_id:
            systems_data = self.systems_id.self_jsonify()
        else:
            systems_data = None
        return jsonify(
                name = self.name,
                Project_id = self.Project_id,
                owner_id = self.owner_id,
                tags = self.tags,
                description = self.description,
                config_data = config_data,
                systems_data = systems_data,
                changed_date = self.changed_date
            ).json

    def jsonify_all():

        nets = ComplexNet.query.all()

        return jsonify([net.self_jsonify() for net in nets])

    @staticmethod
    def get_names():
        try:
            names = ComplexNet.query.with_entities(ComplexNet.name).all()
            return jsonify(status=1, message=None, data=list(*zip(*names)))
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def get_by_id(complex_net_id):
        try:
            complex_net = ComplexNet.query.get(int(complex_net_id))
            return jsonify(status=1, message=None, data=complex_net.self_jsonify())
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def get_by_name(complex_net_name):
        try:
            complex_net = ComplexNet.query.filter_by(name=complex_net_name).first()
            return jsonify(status=1, message=None, data=complex_net.self_jsonify())
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()


    @staticmethod
    def save(json_data):
        try:
            if json_data['name'] in [complex_net.name for complex_net in ComplexNet.query.all()]:
                return jsonify(status=0, message='Not saved! a complex net with this name already exist')
            name = json_data['name']
            project_id = json_data['project_id']
            owner_id = int(json_data['owner_id'])
            tags = json_data['tags']
            description = json_data['description']
            # config_id = int(json_data['config_id'])
            # systems_id = json_data['systems_id']
            # changed_date = datetime.utcnow()

            complex_net = ComplexNet(name, owner_id, tags, description)

            db.session.add(complex_net)
            db.session.commit()

            return jsonify(status= 1, message='complex net '  + complex_net.name + ' succesfully saved')
        except Exception as error:
            return jsonify(status=0, message='Not saved! something went wrong - please try again later')
        finally:
            db.session.close()

    @staticmethod
    def delete_by_name(name):
        try:
            complex_net = ComplexNet.query.filter_by(name=name,project=session['current_project_id']).first()
            if complex_net:
                db.session.delete(complex_net)
                db.session.commit()
                return jsonify(status=1,message='complex net ' + name + ' succefully deleted')
            else:
                return jsonify(status=0,message='Not deleted! No complex net with this name')
        except:
            return jsonify(status=0,message='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def delete_by_id(complex_net_id):
        try:
            complex_net = ComplexNet.query.get(int(complex_net_id))
            if complex_net:
                db.session.delete(complex_net)
                db.session.commit()
                return jsonify(status=1,message='complex net ' + name + ' succefully deleted')
            else:
                return jsonify(status=0,message='Not deleted! No complex net with this id')
        except:
            return jsonify(status=0,message='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def update_by_name(name, json_data):
        try:
            complex_net = ComplexNet.query.filter_by(name=name).first()
            if complex_net:
                complex_net.name = json_data['name']
                complex_net.owner_id = int(json_data['owner_id'])
                complex_net.tags = json_data['tags']
                complex_net.description = json_data['description']
                # complex_net.config_id = int(json_data['stage_id'])
                # complex_net.system_id = json_data['stage_type']
                complex_net.changed_date = datetime.utcnow()

                owner_id = User.query.get(int(ComplexNet.owner_id)).id
                if owner_id:
                    complex_net.changed_by = owner_id
                else:
                    return jsonify(status=0,message='Not updated! No user with given name')
                db.session.add(complex_net)
                db.session.commit()
                return jsonify(status=1,message='complex net ' + complex_net.name + ' succesfully updated')
            else:
                return jsonify(status=0,message='Not deleted! No complex net with this name')


            return jsonify(status= 1, message='complex net '  + ComplexNet.name + ' succesfully updated')
        except Exception as error:
            return jsonify(status=0, message='Not updated! something went wrong - please try again later')
        finally:
            db.session.close()

    @staticmethod
    def update_by_id(complex_net_id, json_data):
        try:
            complex_net = ComplexNet.query.get(int(complex_net_id))
            if complex_net:
                complex_net.name = json_data['name']
                complex_net.owner_id = int(json_data['owner_id']),
                complex_net.tags = json_data['tags'],
                complex_net.description = json_data['description'],
                # complex_net.config_id = int(json_data['config_id']),
                # complex_net.system_id = json_data['system_id'],
                complex_net.changed_date = datetime.utcnow()

                owner_id = User.query.get(int(complex_net.owner_id)).id
                if owner_id:
                    complex_net.changed_by = owner_id
                else:
                    return jsonify(status=0,msg='Not updated! No user with given name')
                db.session.add(complex_net)
                db.session.commit()
                return jsonify(status=1,msg='complex net ' + complex_net.name + ' succesfully updated')
            else:
                return jsonify(status=0,msg='Not deleted! No complex net with this name')


            return jsonify(status= 1, message='complex net '  + complex_net.name + ' succesfully updated')
        except Exception as error:
            return jsonify(status=0, message='Not updated! something went wrong - please try again later')
        finally:
            db.session.close()


class NetConfig(db.Model):
    __tablename__ = 'NetConfig'
    id = db.Column(db.Integer, primary_key=True)
    Lnk_System = db.Column(db.Text)
    Link_Ext_Simulation = db.Column(db.Integer)
    Smiulation_Watch = db.Column(db.Text)
    Simulation_Dis = db.Column(db.Text)
    Simulation_Ext_Flag = db.Column(db.Integer)
    Backup_Env = db.Column(db.Text)
    Backup_Env_Ext_Flag = db.Column(db.Integer)
    Complex_Net_ID = db.Column(db.Integer, db.ForeignKey('ComplexNet.id'))

    def __init__(self,Lnk_System, Link_Ext_Simulation, Smiulation_Watch, Simulation_Dis,
                 Simulation_Ext_Flag, Backup_Env, Backup_Env_Ext_Flag, Complex_Net_ID):
        self.Lnk_System = Lnk_System
        self.Link_Ext_Simulation = Link_Ext_Simulation
        self.Smiulation_Watch = Smiulation_Watch
        self.Simulation_Dis = Simulation_Dis
        self.Simulation_Ext_Flag = Simulation_Ext_Flag
        self.Backup_Env = Backup_Env
        self.Backup_Env_Ext_Flag = Backup_Env_Ext_Flag
        self.Complex_Net_ID = Complex_Net_ID

    def self_jsonify(self):

        return jsonify(
                id = self.id,
                Lnk_System = self.Lnk_System,
                Link_Ext_Simulation = self.Link_Ext_Simulation,
                Smiulation_Watch = self.Smiulation_Watch,
                Simulation_Dis = self.Simulation_Dis,
                Simulation_Ext_Flag = self.Simulation_Ext_Flag,
                Backup_Env = self.Backup_Env,
                Backup_Env_Ext_Flag = self.Backup_Env_Ext_Flag,
                Complex_Net_ID = self.Complex_Net_ID
            ).json

    @staticmethod
    def get_by_id(net_config_id):
        try:
            net_config = NetConfig.query.get(int(net_config_id))
            return jsonify(status=1, message=None, data=net_config.self_jsonify())
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def save(json_data):
        try:
            Lnk_System = json_data['Lnk_System']
            Link_Ext_Simulation = int(json_data['Link_Ext_Simulation'])
            Smiulation_Watch = json_data['Smiulation_Watch']
            Simulation_Dis = json_data['Simulation_Dis']
            Simulation_Ext_Flag = int(json_data['Simulation_Ext_Flag'])
            Backup_Env = json_data['Backup_Env']
            Backup_Env_Ext_Flag = int(json_data['Backup_Env_Ext_Flag'])
            Complex_Net_ID = int(json_data['Complex_Net_ID'])


            net_config = NetConfig(Lnk_System, Link_Ext_Simulation, Smiulation_Watch, Simulation_Dis,
                 Simulation_Ext_Flag, Backup_Env, Backup_Env_Ext_Flag, Complex_Net_ID)

            db.session.add(net_config)
            db.session.commit()

            return jsonify(status= 1)
        except Exception as error:
            return jsonify(status=0, message='Not saved! something went wrong - please try again later')
        finally:
            db.session.close()

    @staticmethod
    def delete_by_id(net_config_id):
        try:
            net_config = NetConfig.query.get(int(net_config_id))
            if net_config:
                db.session.delete(net_config)
                db.session.commit()
                return jsonify(status=1)
            else:
                return jsonify(status=0,message='Not deleted! No net config with this id')
        except:
            return jsonify(status=0,message='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def update_by_id(net_config_id, json_data):
        try:
            net_config = NetConfig.query.get(int(net_config_id))
            if net_config:
                net_config.Link_Ext_Simulation = json_data['Link_Ext_Simulation']
                net_config.Smiulation_Watch = int(json_data['Smiulation_Watch'])
                net_config.Simulation_Dis = json_data['Simulation_Dis']
                net_config.Simulation_Ext_Flag = int(json_data['Simulation_Ext_Flag'])
                net_config.Backup_Env = json_data['Backup_Env']
                net_config.Backup_Env_Ext_Flag = int(json_data['Backup_Env_Ext_Flag'])
                net_config.Complex_Net_ID = int(json_data['Complex_Net_ID'])

                complex_net_id = ComplexNet.query.get(int(net_config.Complex_Net_ID)).id
                if complex_net_id:
                    net_config.Complex_Net_ID = complex_net_id
                else:
                    return jsonify(status=0,msg='Not updated! complex net id')
                db.session.add(net_config)
                db.session.commit()

            return jsonify(status= 1)
        except Exception as error:
            return jsonify(status=0, message='Not updated! something went wrong - please try again later')
        finally:
            db.session.close()

class NetSystem(db.Model):
    __tablename__ = 'NetSystem'
    id = db.Column(db.Integer, primary_key=True)
    system_type = db.Column(db.Text)
    system_num = db.Column(db.Integer)
    kind = db.Column(db.Text)
    Complex_Net_ID = db.Column(db.Integer, db.ForeignKey('ComplexNet.id'))

    def __init__(self,system_type, system_num, kind, Complex_Net_ID):
        self.system_type = system_type
        self.system_num = system_num
        self.kind = kind
        self.Complex_Net_ID = Complex_Net_ID

    def self_jsonify(self):

        return jsonify(
                id = self.id,
                system_type = self.system_type,
                system_num = self.system_num,
                kind = self.kind,
                Complex_Net_ID = self.Complex_Net_ID
            ).json

    @staticmethod
    def get_by_id(net_system_id):
        try:
            net_system = NetSystem.query.get(int(net_system_id))
            return jsonify(status=1, message=None, data=net_system.self_jsonify())
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def save(json_data):
        try:

            system_type = json_data['system_type']
            system_num = int(json_data['system_num'])
            kind = json_data['kind']
            Complex_Net_ID = int(json_data['Complex_Net_ID'])


            net_system = NetSystem(system_type, system_num, kind, Complex_Net_ID)

            db.session.add(net_system)
            db.session.commit()

            return jsonify(status= 1)
        except Exception as error:
            return jsonify(status=0, message='Not saved! something went wrong - please try again later')
        finally:
            db.session.close()

    @staticmethod
    def delete_by_id(net_system_id):
        try:
            net_system = NetSystem.query.get(int(net_system_id))
            if net_system:
                db.session.delete(net_system)
                db.session.commit()
                return jsonify(status=1)
            else:
                return jsonify(status=0,message='Not deleted! No net system with this id')
        except:
            return jsonify(status=0,message='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def update_by_id(net_system_id, json_data):
        try:
            net_system = NetSystem.query.get(int(net_system_id))
            if net_system:
                net_system.system_type = json_data['system_type']
                net_system.system_num = int(json_data['system_num'])
                net_system.kind = json_data['kind']
                net_system.Complex_Net_ID = int(json_data['Complex_Net_ID'])

                complex_net_id = ComplexNet.query.get(int(net_system.Complex_Net_ID)).id
                if complex_net_id:
                    net_system.Complex_Net_ID = complex_net_id
                else:
                    return jsonify(status=0,msg='Not updated! complex net id')
                db.session.add(net_system)
                db.session.commit()

            return jsonify(status= 1)
        except Exception as error:
            return jsonify(status=0, message='Not updated! something went wrong - please try again later')
        finally:
            db.session.close()

class StageRunMani(db.Model):
    __tablename__ = 'StageRunMani'
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.Text)
    owner_id = db.Column(db.Integer)
    tags = db.Column(db.Text)
    description = db.Column(db.Text)
    concequences = db.Column(db.Text)
    complex_net_id = db.Column(db.Integer)
    site_id = db.Column(db.Integer)
    net = db.Column(db.Text)
    scenario_folder = db.Column(db.Text)
    scenario_file = db.Column(db.Text)
    is_run_all_scenarios = db.Column(db.Boolean)
    dp_folder = db.Column(db.Text)
    dp_file = db.Column(db.Text)
    ovr_file = db.Column(db.Text)
    run_time = db.Column(db.Integer)
    is_auto_user_cmd = db.Column(db.Boolean)
    user_cmd_file = db.Column(db.Text)
    is_fmc = db.Column(db.Boolean)
    fmc_config_file = db.Column(db.Text)
    fmc_connection_file = db.Column(db.Text)
    fmc_scenario_file = db.Column(db.Text)
    is_env_shutdown = db.Column(db.Boolean)
    env_shutdown_time = db.Column(db.Integer)
    changed_date = db.Column(db.DateTime)

    def __init__(self,name, owner_id, tags, description, concequences, complex_net_id, site_id, net,
                 scenario_folder, scenario_file, is_run_all_scenarios, dp_folder, dp_file, ovr_file,
                 run_time, is_auto_user_cmd, user_cmd_file, is_fmc, fmc_config_file, fmc_connection_file,
                 fmc_scenario_file, is_env_shutdown, env_shutdown_time):
        self.name  = name
        self.owner_id = owner_id
        self.tags = tags
        self.description = description
        self.concequences = concequences
        self.complex_net_id = complex_net_id
        self.site_id = site_id
        self.net = net
        self.scenario_folder = scenario_folder
        self.scenario_file = scenario_file
        self.is_run_all_scenarios = is_run_all_scenarios
        self.dp_folder = dp_folder
        self.dp_file = dp_file
        self.ovr_file = ovr_file
        self.run_time = run_time
        self.is_auto_user_cmd = is_auto_user_cmd
        self.is_fmc = is_fmc
        self.fmc_config_file = fmc_config_file
        self.fmc_connection_file = fmc_connection_file
        self.fmc_scenario_file = fmc_scenario_file
        self.is_env_shutdown = is_env_shutdown
        self.env_shutdown_time = env_shutdown_time
        self.changed_date = datetime.utcnow()

    def self_jsonify(self):
        owner = User.query.get(self.owner_id)
        if owner:
            owner_name = owner.name
        else:
            owner_name = None

        complex_net = ComplexNet.query.get(self.complex_net_id)
        if complex_net:
            complex_net_name = complex_net.name
        else:
            complex_net_name = None

        site = Site.query.get(self.site_id)
        if site:
            site_name = site.name
        else:
            site_name = None


        return jsonify(
                id = self.id,
                name  = self.name,
                owner = owner_name,
                tags = self.tags,
                description = self.description,
                concequences = self.concequences,
                complex_net_name = complex_net_name,
                site_name = site_name,
                net = self.net,
                scenario_folder = self.scenario_folder,
                scenario_file = self.scenario_file,
                is_run_all_scenarios = self.is_run_all_scenarios,
                dp_folder = self.dp_folder,
                dp_file = self.dp_file,
                ovr_file = self.ovr_file,
                run_time = self.run_time,
                is_auto_user_cmd = self.is_auto_user_cmd,
                user_cmd_file = self.user_cmd_file,
                is_fmc = self.is_fmc,
                fmc_config_file = self.fmc_config_file,
                fmc_connection_file = self.fmc_connection_file,
                fmc_scenario_file = self.fmc_scenario_file,
                is_env_shutdown = self.is_env_shutdown,
                env_shutdown_time = self.env_shutdown_time,
                changed_date = self.changed_date
            ).json

    @staticmethod
    def get_by_id(stage_run_mani_id):
        try:
            stage_run_mani = StageRunMani.query.get(int(stage_run_mani_id))
            return jsonify(status=1, message=None, data=stage_run_mani.self_jsonify())
        except Exception as error:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def get_by_name(stage_run_mani_name):
        try:
            stage_run_mani = StageRunMani.query.filter_by(name=stage_run_mani_name).first()
            return jsonify(status=1, message=None, data=stage_run_mani.self_jsonify())
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def save(json_data):
        try:
            owner = User.query.filter_by(name=json_data['changed_by']).first()
            if owner:
                owner_id = owner.id
            else:
                return jsonify(status= 0, message='Not saved! No user named ' + json_data['changed_by'])

            complex_net = ComplexNet.query.filter_by(name=json_data['complex_net_name']).first()
            if complex_net:
                complex_net_id = complex_net.id
            else:
                return jsonify(status= 0, message='Not saved! No complex net named ' + json_data['complex_net_name'])

            site = Site.query.filter_by(name=json_data['site_name']).first()
            if site:
                site_id = site.id
            else:
                return jsonify(status= 0, message='Not saved! No site named ' + json_data['site_name'])

            name  = json_data['name']
            tags = json_data['tags']
            description = json_data['description']
            concequences = json_data['concequences']
            net = json_data['net']
            scenario_folder = json_data['scenario_folder']
            scenario_file = json_data['scenario_file']
            is_run_all_scenarios = json_data['is_run_all_scenarios']
            dp_folder = json_data['dp_folder']
            dp_file = json_data['dp_file']
            ovr_file = json_data['ovr_file']
            run_time = int(json_data['run_time'])
            is_auto_user_cmd = json_data['is_auto_user_cmd']
            user_cmd_file = json_data['user_cmd_file']
            is_fmc = json_data['is_fmc']
            fmc_config_file = json_data['fmc_config_file']
            fmc_connection_file = json_data['fmc_connection_file']
            fmc_scenario_file = json_data['fmc_scenario_file']
            is_env_shutdown = json_data['is_env_shutdown']
            env_shutdown_time = int(json_data['env_shutdown_time'])
            changed_date = datetime.utcnow()


            stage_run_mani = StageRunMani(name, owner_id, tags, description, concequences, complex_net_id, site_id, net,
                 scenario_folder, scenario_file, is_run_all_scenarios, dp_folder, dp_file, ovr_file,
                 run_time, is_auto_user_cmd, user_cmd_file, is_fmc, fmc_config_file, fmc_connection_file,
                 fmc_scenario_file, is_env_shutdown, env_shutdown_time)

            db.session.add(stage_run_mani)
            db.session.commit()

            return jsonify(status= 1, message='Stage ' + stage_run_mani.name + ' successfuly saved')
        except Exception as error:
            return jsonify(status=0, message='Not saved! something went wrong - please try again later')
        finally:
            db.session.close()

    @staticmethod
    def delete_by_id(stage_run_mani_id):
        try:
            stage_run_mani = StageRunMani.query.get(int(stage_run_mani_id))
            if stage_run_mani:
                db.session.delete(stage_run_mani)
                db.session.commit()
                return jsonify(status=1)
            else:
                return jsonify(status=0,message='Not deleted! No net system with this id')
        except:
            return jsonify(status=0,message='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def delete_by_name(name):
        try:
            stage_run_mani = StageRunMani.query.filter_by(name=name,project=session['current_project_id']).first()
            if stage_run_mani:
                db.session.delete(stage_run_mani)
                db.session.commit()
                return jsonify(status=1,msg='stage ' + name + ' succefully deleted')
            else:
                return jsonify(status=0,msg='Not deleted! No stage with this name')
        except:
            return jsonify(status=0,msg='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def update_by_id(stage_run_mani_id, json_data):
        try:
            stage_run_mani = StageRunMani.query.get(int(stage_run_mani_id))
            if stage_run_mani:
                complex_net = ComplexNet.query.filter_by(name=json_data['complex_net_name']).first()
                if complex_net:
                    complex_net_id = complex_net.id
                else:
                    return jsonify(status= 0, message='Not saved! No complex net named ' + json_data['complex_net_name'])

                site = Site.query.filter_by(name=json_data['site_name']).first()
                if site:
                    site_id = site.id
                else:
                    return jsonify(status= 0, message='Not saved! No site named ' + json_data['site_name'])

                name  = json_data['name']
                tags = json_data['tags']
                description = json_data['description']
                concequences = json_data['concequences']
                net = json_data['net']
                scenario_folder = json_data['scenario_folder']
                scenario_file = json_data['scenario_file']
                is_run_all_scenarios = json_data['is_run_all_scenarios']
                dp_folder = json_data['dp_folder']
                dp_file = json_data['dp_file']
                ovr_file = json_data['ovr_file']
                run_time = int(json_data['run_time'])
                is_auto_user_cmd = json_data['is_auto_user_cmd']
                is_fmc = json_data['is_fmc']
                fmc_config_file = json_data['fmc_config_file']
                fmc_connection_file = json_data['fmc_connection_file']
                fmc_scenario_file = json_data['fmc_scenario_file']
                is_env_shutdown = json_data['is_env_shutdown']
                env_shutdown_time = int(json_data['env_shutdown_time'])
                changed_date = datetime.utcnow()

                db.session.add(stage_run_mani)
                db.session.commit()
                return jsonify(status=1,message='stage ' + stage_run_mani.name + ' succesfully updated')
            else:
                return jsonify(status=0,message='Not deleted! No stage with this name')

        except Exception as error:
            return jsonify(status=0, message='Not updated! something went wrong - please try again later')
        finally:
            db.session.close()

    def update_by_name(name, json_data):
        try:
            stage_run_mani = StageRunMani.query.filter_by(name=name).first()
            if stage_run_mani:
                complex_net = ComplexNet.query.filter_by(name=json_data['complex_net_name']).first()
                if complex_net:
                    complex_net_id = complex_net.id
                else:
                    return jsonify(status= 0, message='Not saved! No complex net named ' + json_data['complex_net_name'])

                site = Site.query.filter_by(name=json_data['site_name']).first()
                if site:
                    site_id = site.id
                else:
                    return jsonify(status= 0, message='Not saved! No site named ' + json_data['site_name'])

                name  = json_data['name']
                tags = json_data['tags']
                description = json_data['description']
                concequences = json_data['concequences']
                net = json_data['net']
                scenario_folder = json_data['scenario_folder']
                scenario_file = json_data['scenario_file']
                is_run_all_scenarios = json_data['is_run_all_scenarios']
                dp_folder = json_data['dp_folder']
                dp_file = json_data['dp_file']
                ovr_file = json_data['ovr_file']
                run_time = int(json_data['run_time'])
                is_auto_user_cmd = json_data['is_auto_user_cmd']
                is_fmc = json_data['is_fmc']
                fmc_config_file = json_data['fmc_config_file']
                fmc_connection_file = json_data['fmc_connection_file']
                fmc_scenario_file = json_data['fmc_scenario_file']
                is_env_shutdown = json_data['is_env_shutdown']
                env_shutdown_time = int(json_data['env_shutdown_time'])
                changed_date = datetime.utcnow()

                db.session.add(stage_run_mani)
                db.session.commit()
                return jsonify(status=1,message='stage ' + stage_run_mani.name + ' succesfully updated')
            else:
                return jsonify(status=0,message='Not deleted! No stage with this name')

        except Exception as error:
            return jsonify(status=0, message='Not updated! something went wrong - please try again later')
        finally:
            db.session.close()


class RunList(db.Model):
    __tablename__ = 'RunList'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    db_name = db.Column(db.Text)
    run_id = db.Column(db.Integer)
    scenario_name = db.Column(db.Text)
    project = db.Column(db.Integer)

    def __init__(self,name, db_name, run_id, scenario_name, project):
        self.name = name
        self.db_name = db_name
        self.run_id = run_id
        self.scenario_name = scenario_name
        self.project = project

    def self_jsonify(self):
        return jsonify(
            name = self.name,
            db_name = self.db_name,
            scenario_name = self.scenario_name,
            project = Project.query.get(self.project).name
        ).json

    @staticmethod
    def get_by_name(run_list_name):
        try:
            run_list = RunList.query.filter_by(name=run_list_name, project=session['current_project_id']).all()
            return jsonify(status=1, message=None, data=[run.self_jsonify() for run in run_list])
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def get_num_of_runs_by_name(run_list_name):
        try:
            run_list = RunList.query.filter_by(name=run_list_name, project=session['current_project_id']).all()
            return jsonify(status=1, message=None, data=len(run_list))
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    def save(json_data):
        if 'run_ids' not in json_data:
            return jsonify(status=0,message="did not find 'run_ids' field in sent data")
        if 'name' not in json_data:
            return jsonify(status=0,message="did not find 'name' field in sent data")

        project = session['current_project_id']
        name = json_data['name']
        names = [l_name for l_name in RunList.query.filter_by(name=name, project=project).with_entities(RunList.name).distinct()]
        names = list(*zip(*names))
        if name in names:
            return jsonify(status=0,message="list name already exist!")
        run_ids = json_data['run_ids']
        try:
            [db.session.add(RunList(
                                    name=name,
                                    db_name=run['db'],
                                    run_id=int(run['run_id']),
                                    scenario_name=run['scenario'],
                                    project=project
                                    ))
             for run in run_ids]
        except:
            db.session.rollback()
            return jsonify(status=0,message="something went wrong while logging the run_ids")
        try:
            if 'lists' in json_data:
                lists = json_data['lists']
                for curr_list in lists:
                    list_data = RunList.query.filter_by(name=curr_list, project=project).all()
                    [db.session.add(RunList(
                                    name=name,
                                    db_name=run.db_name,
                                    run_id=int(run.run_id),
                                    scenario_name=run.scenario_name,
                                    project=project
                                    ))
                    for run in list_data]
        except:
            db.session.rollback()
            return jsonify(status=0,message="something went wrong while logging the run_ids from a given list")
        try:      
            db.session.commit()
            return jsonify(status=1,message="")
        except:
            db.session.rollback()
            return jsonify(status=0,message="something went wrong while commiting to db")

    def get_names():
        try:
            names = [run.name for run in RunList.query.filter_by(project=session['current_project_id']).with_entities(RunList.name).distinct()]
            message = ""
            status = 1
        except:
            names = []
            message = "something went wrong"
            status = 0
        finally:
            return jsonify(status=status,message=message ,data=names)

    def get_names_json():
        try:
            names = [{"name":run.name} for run in RunList.query.filter_by(project=session['current_project_id']).with_entities(RunList.name).distinct()]
            message = ""
            status = 1
        except:
            names = []
            message = "something went wrong"
            status = 0
        finally:
            return jsonify(status=status,message=message ,data=names)

class AnalyseSetup(db.Model):
    __tablename__ = 'AnalyseSetup'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    functions = db.relationship('OctopusFunction', secondary=SetupsAndFunctions,
                                backref=db.backref('functions', lazy='dynamic'))
    groups = db.relationship('FunctionsGroup', secondary=SetupsAndGroups,
                                backref=db.backref('groups', lazy='dynamic'))
    runs = db.relationship('SetupRuns', secondary=SetupsAndRuns,
                                backref=db.backref('AnalyseSetup', lazy='dynamic'))
    run_lists = db.relationship('RunList', secondary=SetupsAndRunLists,
                                backref=db.backref('AnalyseSetup', lazy='dynamic'))
    project = db.Column(db.Integer)

    def __init__(self,name,run_lists=[],runs=[],functions=[], groups=[], project=None):
        self.name = name
        self.runs = runs
        self.run_lists = run_lists
        self.functions = functions
        self.groups = groups
        self.project = project



    def self_jsonify(self):
        runs = {}
        for run in self.runs:
            if run.db_name in runs:
                runs[run.db_name][str(run.run_id)] = run.scenario_name
            else:
                runs[run.db_name] = {}
                runs[run.db_name][str(run.run_id)] = run.scenario_name
        return jsonify(
            name = self.name,
            runs = runs,
            run_lists = list(set([run_list.name for run_list in self.run_lists])),
            functions = [function.name for function in self.functions],
            groups = [group.name for group in self.groups]
        ).json

    @staticmethod
    def get_by_name(setup_name):
        try:
            project = AnalyseSetup.query.filter_by(name=setup_name, project=session['current_project_id']).first()
            return jsonify(status=1, message=None, data=project.self_jsonify())
        except:
            return jsonify(status=0, message='something went wrong', data=None)
        finally:
            db.session.close()

    @staticmethod
    def save(json_data):
        try:
            # setting up expected data structure
            extracted_data = {"name":None, "runs":[], "run_lists": [], "functions":[], "groups":[]}

            # extracting data - return error message if one of the keys is not found
            for key in extracted_data.keys():
                if key in json_data:
                    extracted_data[key] = json_data[key]
                else:
                    return jsonify(status=0,message=["did not find " + key + " in sent data"], data=None)
            if len(extracted_data['name']) == 0:
                return jsonify(status=0,message=["cannot update! name cannot be empty"], data=None)

            # setting up error_messages and setup object
            if extracted_data['name'] in [setup.name for setup in AnalyseSetup.query.filter_by(project=session['current_project_id']).all()]:
                return jsonify(status=0,message=["cannot save! name " + extracted_data['name'] + " already exist"], data=None)

            if re.search('[^\w_-]',extracted_data["name"]) or extracted_data["name"][0].isdigit():
                return jsonify(status=0,message=["error! name may only start with a letter, contain letters, numbers and the '-' and '_' signs"], data=None)

            if type(extracted_data["name"]) == type(str(1)):
                if re.search('[^\w_-]',extracted_data["name"]):
                     return jsonify(status=0,message=["error! name may only contain letters, numbers and the '-' and '_' signs"], data=None)
            else:
                return jsonify(status=0,message=["error! name must be a string"], data=None)
            error_messages = []
            setup = AnalyseSetup(name=json_data['name'], project=session['current_project_id'])
            setup.run_lists = []
            setup.functions = []
            setup.groups = []
            setup.runs = []
            # extracting object from identifiers and appending to setup object
            for key in extracted_data.keys():
                if not key == "name":
                    if key == "runs":
                        setup.append_runs(extracted_data[key])
                    elif type(extracted_data[key]) == type([]):
                        [
                            error_messages.append(setup.append_object_by_identifier(obj, key))
                            for obj in extracted_data[key]
                        ]
                    else:
                        return jsonify(status=0,message=["input run lists identifiers must be an array"], data=None)

            # clearing None entries from error_messages
            error_messages = [message for message in error_messages if message]

            #commit if there are no error messages. otherwise, return error
            if error_messages:
                db.session.rollback()
                return jsonify(status=0,message=error_messages, data=None)
            db.session.add(setup)
            db.session.commit()
            return jsonify(status=1,message=[], data=None)
        except:
            db.session.rollback()
            return jsonify(status=0,message=["something went wrong"], data=None)

    @staticmethod
    def update_by_name(name, json_data):
        try:
            # setting up expected data structure
            extracted_data = {"new_name":None, "runs":[] ,"run_lists": [], "functions":[], "groups":[]}

            # extracting data - return error message if one of the keys is not found
            for key in extracted_data.keys():
                if key in json_data:
                    extracted_data[key] = json_data[key]
                else:
                    return jsonify(status=0,message=["did not find " + key + " in sent data"], data=None)
            if len(extracted_data['new_name']) == 0:
                return jsonify(status=0,message=["cannot update! new name cannot be empty"], data=None)
            # setting up error_messages and setup object
            if not name in [setup.name for setup in AnalyseSetup.query.filter_by(project=session['current_project_id']).all()]:
                return jsonify(status=0,message=["cannot update! no setup with this name"], data=None)

            if re.search('[^\w_-]',extracted_data["new_name"]) or extracted_data["new_name"][0].isdigit():
                return jsonify(status=0,message=["error! name may only start with a letter, contain letters, numbers and the '-' and '_' signs"], data=None)

            error_messages = []
            setup = AnalyseSetup.query.filter_by(name=name, project=session['current_project_id']).first()
            setup.run_lists = []
            setup.functions = []
            setup.groups = []
            setup.runs = []
            # extracting object from identifiers and appending to setup object
            for key in extracted_data.keys():
                if key not in ["name", "new_name"]:
                    if key == "runs":
                        setup.append_runs(extracted_data[key])
                    elif type(extracted_data[key]) == type([]):
                        [
                            error_messages.append(setup.append_object_by_identifier(obj, key))
                            for obj in extracted_data[key]
                        ]
                    else:
                        return jsonify(status=0,message=["input " + key + " identifiers must be an array"], data=None)
                elif key == "runs":
                    setup.append_runs(extracted_data[key])
            setup.name = extracted_data['new_name']
            # clearing None entries from error_messages
            error_messages = [message for message in error_messages if message]

            #commit if there are no error messages. otherwise, return error
            if error_messages:
                db.session.rollback()
                return jsonify(status=0,message=error_messages, data=None)
            db.session.add(setup)
            db.session.commit()
            return jsonify(status=1,message=[], data=None)
        except:
            db.session.rollback()
            return jsonify(status=0,message=["something went wrong"], data=None)

    @staticmethod
    def update_by_id(setup_id, json_data):
        try:
            # setting up expected data structure
            extracted_data = {"new_name":None ,"run_lists": [], "functions":[], "groups":[]}

            # extracting data - return error message if one of the keys is not found
            for key in extracted_data.keys():
                if key in json_data:
                    extracted_data[key] = json_data[key]
                else:
                    return jsonify(status=0,message=["did not find " + key + " in sent data"], data=None)
            if len(extracted_data['new_name']) == 0:
                return jsonify(status=0,message=["cannot update! new name cannot be empty"], data=None)
            # setting up error_messages and setup object
            setup = AnalyseSetup.query.get(setup_id)
            if setup:
                return jsonify(status=0,message=["cannot update! no setup with this id"], data=None)

            if re.search('[^\w_-]',extracted_data["new_name"]) or extracted_data["new_name"][0].isdigit():
                return jsonify(status=0,message=["error! name may only start with a letter, contain letters, numbers and the '-' and '_' signs"], data=None)

            error_messages = []
            setup.run_lists = []
            setup.functions = []
            setup.groups = []
            setup.runs = []
            # extracting object from identifiers and appending to setup object
            for key in extracted_data.keys():
                if key not in ["name", "new_name"]:
                    if key == "runs":
                        setup.append_runs(extracted_data[key])
                    elif type(extracted_data[key]) == type([]):
                        [
                            error_messages.append(setup.append_object_by_identifier(obj, key))
                            for obj in extracted_data[key]
                        ]
                    else:
                        return jsonify(status=0,message=["input " + key + " identifiers must be an array"], data=None)

            setup.name = extracted_data['new_name']
            # clearing None entries from error_messages
            error_messages = [message for message in error_messages if message]

            #commit if there are no error messages. otherwise, return error
            if error_messages:
                db.session.rollback()
                return jsonify(status=0,message=error_messages, data=None)
            db.session.add(setup)
            db.session.commit()

            return jsonify(status=1,message=[], data=None)
        except:
            db.session.rollback()
            return jsonify(status=0,message=["something went wrong"], data=None)

    def append_runs(self, runs):
        for run in runs:
            run_obj = SetupRuns.query.filter_by(run_id=run['run_id'], db_name=run['db_name'],
                                                project=session['current_project_id']).first()
            if run_obj:
                self.runs.append(run_obj)
            else:
                run_obj = SetupRuns(run_id=run['run_id'], db_name=run['db_name'], 
                                    scenario_name=run['scenario_name'], 
                                    project=session['current_project_id'])
                db.session.add(run_obj)
                self.runs.append(run_obj)

    def append_object_by_identifier(self, identifer, obj_type):
        message = None
        if type(identifer) == type(str(1)):
            if identifer.isdigit():
                identifer = int(identifer)
                method = 'get'
            else:
                method = 'filter'
        elif type(identifer) == type(int(1)):
            method = 'get'
        else:
            message = 'error! idnetifer must be the object id name'
            return message
        if obj_type == 'groups':
            query_obj = FunctionsGroup.query
        elif obj_type == 'functions':
            query_obj = OctopusFunction.query
        elif obj_type == 'run_lists':
            query_obj = RunList.query
        else:
            message = 'error! unidentified object type'
        if method == 'get':
            obj_to_append = query_obj.get(identifer)
        else:
            if obj_type == 'run_lists':
                obj_to_append = query_obj.filter_by(name=identifer, project=session['current_project_id']).all()
            else:
                obj_to_append = query_obj.filter_by(name=identifer, project=session['current_project_id']).first()
        if obj_to_append:
            if obj_type == 'groups':
                self.groups.append(obj_to_append)
            elif obj_type == 'functions':
                self.functions.append(obj_to_append)
            else:
                [self.run_lists.append(obj) for obj in obj_to_append]
        else:
            message = 'error! no object with given identifier' + str(identifer)

        return message

    def get_names():
        try:
            names = [setup.name for setup in AnalyseSetup.query.filter_by(project=session['current_project_id']).with_entities(AnalyseSetup.name).all()]
            message = ""
            status = 1
        except:
            names = []
            message = "something went wrong"
            status = 0
        finally:
            return jsonify(status=status,message=message ,data=names)

    @staticmethod
    def delete_by_id(setup_id):
        try:
            setup = AnalyseSetup.query.get(int(setup_id))
            if setup:
                db.session.delete(setup)
                db.session.commit()
                return jsonify(status=1,msg='setup with id:' + setup_id + ' succefully deleted')
            else:
                return jsonify(status=0,message='Not deleted! No setup with this id')
        except:
            return jsonify(status=0,message='Not deleted! Something went wrong in the delete process')
        finally:
            db.session.close()

    @staticmethod
    def delete_by_name(name):
        try:
            setup = AnalyseSetup.query.filter_by(name=name,project=session['current_project_id']).first()
            if setup:
                setup.run_lists = []
                setup.functions = []
                setup.groups = []
                setup.runs = []
                db.session.commit()
                db.session.delete(setup)
                db.session.commit()
                return jsonify(status=1,msg='setup ' + name + ' succefully deleted')
            else:
                return jsonify(status=0,msg='Not deleted! No setup with this name')
        except:
            db.session.rollback()
            return jsonify(status=0,msg='Not deleted! Something went wrong in the delete process')
        # finally:
        #     db.session.close()

    def get_func_ids(self):
        group_func_ids = []
        for group in self.groups:
            curr_ids = group.get_functions_ids()
            if curr_ids:
                group_func_ids += curr_ids
        func_ids = [func.id for func in self.functions]

        return list(set(func_ids+group_func_ids))
    
    def get_dbs_and_runs(self):
        dbs = {}
        return [{"db_name":run.db_name, "run_id":run.run_id, "scenario_name":run.scenario_name}
        for run in self.run_lists+self.runs]
        
    def create_mission(self, tasks_queue):
        # creating the mission
        project = project=session['current_project_id']
        user_name = session['username']
        user_id = User.query.filter_by(name=user_name).first().id
        mission = Mission(self.name + '_' + user_name, project=project)
        db.session.add(mission)
        db.session.commit()
        mission.name = mission.name + '_' + str(mission.id)
        db.session.commit()
        # getting functions ids
        functions_ids = self.get_func_ids()
        
        # getting runs and connections
        functions_dict = {"run_id":list, "scenario_name":list}
        df=pd.DataFrame(self.get_dbs_and_runs()).groupby('db_name').aggregate(functions_dict)

        for db_name, row in df.iterrows():
            conn = DbConnector.load_conn_by_name(db_name)
            if conn.status == 'valid':
                db_status = 1
                db_run_ids = conn.get_run_ids(db_name).json['run_ids']
            else:
                db_status = -1
            for index, run_id in enumerate(row.run_id):
                for func_id in functions_ids:
                    scenario_name = row.scenario_name[index]
                    run_status = db_status
                    if run_status > 0:
                        if run_id not in db_run_ids:
                            run_status = -2
                    task = Task(mission.id, conn, run_id, run_status, scenario_name, func_id, user_id)
                    tasks_queue.put_nowait(task)

        return {"status":1,"message":'task id is'+str(mission.id)}
class SetupRuns(db.Model):
    __tablename__ = 'SetupRuns'
    id = db.Column(db.Integer, primary_key=True)
    db_name = db.Column(db.Text)
    run_id = db.Column(db.Integer)
    scenario_name = db.Column(db.Text)
    project = db.Column(db.Integer)

    def __init__(self, db_name, run_id, scenario_name, project):
        self.db_name = db_name
        self.run_id = run_id
        self.scenario_name = scenario_name
        self.project = project

    def self_jsonify(self):
        return jsonify(
            run_id = self.run_id,
            db_name = self.db_name,
            scenario_name = self.scenario_name,
            project = Project.query.get(self.project).name
        ).json