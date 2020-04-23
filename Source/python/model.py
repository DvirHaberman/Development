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

def init_db():
    db = SQLAlchemy()
    return db

def create_threaded_app(db):
    threaded_app = Flask(__name__)
    db.init_app(threaded_app)
    threaded_app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://dvirh:dvirh@localhost:3306/octopusdb"
    threaded_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return threaded_app
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
                self.connection = create_engine(self.conn_string, connect_args={'connect_timeout': 10})
                conn = self.connection.connect()
                conn.close()
                self.connection.dispose()
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
        if DbConnections.query.filter_by(name=self.name).first():
            self.message = 'cannot save - db name already exist'
            self.status = 'invalid'
            return
        # saving connection data to DB
        try:
            conn = DbConnections(self.db_type, self.user, self.password, self.hostname, self.port, self.schema, self.name, self.conn_string)
            db.session.add(conn)
            db.session.commit()
        except Exception as error:
            self.message = 'Something when wrong while saving to DB.'
            self.status = 'invalid'
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
    def get_sys_params():
        return 'Sys_Params'
    
    @staticmethod
    def get_test_params():
        return 'Test_Params'

    @staticmethod
    def get_db_conn(db_name):
        return 'db_conn for'+ db_name




########################################
########### TASK CLASS ############
########################################


class Task:

    def __init__(self, mission_id, db_conn_obj, run_id, function_id, user_id, task_id=0, priority=1, status=0):
        self.id=task_id
        self.mission_id=mission_id
        self.db_conn_obj = db_conn_obj
        self.run_id = run_id
        self.function_id = function_id
        self.user_id = user_id
        self.priority = priority
        self.status = status

    def log(self):
        task = AnalyseTask(mission_id=self.mission_id, mission_type=0, function_id=self.function_id,
                 run_id=self.run_id, scenario_id=None, ovr_file_location=None, db_conn_string=self.db_conn_obj.conn_string,
                 priority=1, user_id=self.user_id, status=0)
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


#########################################
########### USER MODEL CLASS ############
#########################################

class User(db.Model):
    __tablename__ = "Users"
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
    project = db.Column(db.Integer, db.ForeignKey('Project.id'))

    def __init__(self, name=None, first_name=None, last_name=None, password_sha=None, state=None,
                 role=None, team=None, functions=[], max_priority=None, project=None):
        self.name = name
        self.first_name = first_name
        self.last_name = last_name
        self.password_sha = password_sha
        self.state = state
        self.role = role
        self.team = team
        self.functions = functions
        self.max_priority = max_priority
        self.project = project
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
            project=Project.query.get(self.project).name
        ).json

    @staticmethod
    def jsonify_all():
        table = User.query.all()
        return jsonify([row.self_jsonify() for row in table])

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
    version = db.Column(db.Text)
    users = db.relationship('User', backref='Project', lazy=True)

    def __init__(self, name=None, version=None, users=[]):
        self.name = name
        self.version = version
        self.users = users

    def self_jsonify(self):
        return jsonify(
            name=self.name,
            version=self.version,
            users=jsonify([user.self_jsonify() for user in self.users]).json
        ).json


#####################################################
######### FunctionParameters MODEL CLASS ############
#####################################################


class FunctionParameters(db.Model):
    __tablename__ = 'FunctionParameters'
    id = db.Column(db.Integer, primary_key=True)
    function_id = db.Column(db.Integer, db.ForeignKey('OctopusFunctions.id'))
    kind = db.Column(db.Text)
    value = db.Column(db.Text)
    type = db.Column(db.Text)

    def __init__(self, function_id=None, kind=None, value=None, type=None):
        self.function_id = function_id
        self.kind = kind
        self.value = value
        self.type = type
    def self_jsonify(self):
        return jsonify(
            function_id=self.function_id,
            kind=self.kind,
            value=self.value,
            type=self.type
        ).json

    @staticmethod
    def jsonify_all():
        table = FunctionParameters.query.all()
        return jsonify([row.self_jsonify() for row in table])

    def get_value(self):
        if self.kind == 'Sys_Params':
            return OctopusUtils.get_sys_params()
        
        if self.kind == 'Test_Params':
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
########### OCTOPUSFUNCTIONS MODEL CLASS ############
#####################################################


class OctopusFunction(db.Model):
    __tablename__ = "OctopusFunctions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    callback = db.Column(db.Text)
    file_name = db.Column(db.Text)
    location = db.Column(db.Text)
    owner = db.Column(db.Integer, db.ForeignKey('Users.id'))
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

    def __init__(self, name=None, callback=None, file_name=None, location=None, owner=None, status=None, tree=None,
                 kind=None, tags=None, description=None, version_comments=None,  is_class_method=None, class_name=None,
                 function_checksum=None, version=None, handler_checksum=None, function_parameters=[], changed_date=datetime.utcnow(), is_locked=0):
        self.name = name
        self.callback = callback
        self.file_name = file_name
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
            function_parameters=jsonify([param.self_jsonify() for param in self.function_parameters]).json
        ).json

    @staticmethod
    def save_function(data):
        func = OctopusFunction(
            name=data['name'],
            callback=data['callback'],
            location=data['location'],
            owner=User.query.filter_by(name=data['owner'])[0].name,
            # status=data.status,
            # tree=row.tree,
            kind=data['kind'],
            tags=data['tags'],
            description=data['description'],
            # project=row.project,
            version=data['version'],
            version_comments=data['version_comments'],
            function_checksum=22,
            handler_checksum=33,
            # is_locked=row.is_locked
        )
        db.session.add(func)
        db.session.commit()
        return func.self_jsonify()

    @staticmethod
    def jsonify_all():
        table = OctopusFunction.query.all()
        return jsonify([row.self_jsonify() for row in table])
    
    def run(self, db_conn, run_id):
        #check if path is in os.path
        try:
            if not self.location in sys.path:
                return {   
                    'run_id': run_id,
                    'db_conn': db_conn.name,
                    'result_status':1, 
                    'result_text':'Error! Function file is not included in Octopus Path', 
                    'result_arr' : None
                }
            #check if file is in path
            if not Path(self.location).exists():
                return {
                    'run_id': run_id,
                    'db_conn': db_conn.name,
                    'result_status':1, 
                    'result_text':'Error! Function module is not in the specified location', 
                    'result_arr' : None
                }
            #import module
            module = importlib.import_module(self.file_name.split('.')[0])
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
                    'result_arr' : None
                }
            #else - check for function
            else:
                req_method = getattr(module, self.callback)
        except:
            return {
                'run_id': run_id,
                'db_conn': db_conn.name,
                'result_status':1, 
                'result_text':'Error! Unexpected error while extracting the method', 
                'result_arr' : None
            }
        try:
            parameters_tuple = self.get_parameters_tuple()
        except:
            return {
                'run_id': run_id,
                'db_conn': db_conn,
                'result_status':1, 
                'result_text':"Error! Unexpected error while extracting method's parameters", 
                'result_arr' : None
            }

        try:
            if len(parameters_tuple) > 0:
                result_dict = req_method(db_conn, run_id, *parameters_tuple)
            else:
                result_dict = req_method(db_conn, run_id)
            result_dict.update([('run_id', run_id), ('db_conn', db_conn.name)])
            return result_dict
        except Exception as error:
            return {
                'run_id': run_id,
                'db_conn': db_conn.name,
                'result_status':1, 
                'result_text':'Error! Unexpected error while activating the method', 
                'result_arr' : None
            }

    # def __repr__(self):
    #     print(f'my name is {self.name} and my owner is {self.owner}')

    # def printme(self):
    #     return f'my name is {self.name} and my owner is {self.owner}'

    def get_parameters_tuple(self):
        params_tuple = [param.get_value() for param in self.function_parameters]
        return params_tuple

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
    functions = db.relationship('OctopusFunction', secondary=FunctionsAndGroups,
                                backref=db.backref('groups', lazy='dynamic'))

    def __init__(self, name=None, functions=[]):
        self.name = name
        self. functions = functions

    def self_jsonify(self):
        return jsonify(
            id=self.id,
            name=self.name,
            functions=jsonify([func.name for func in self.functions]).json
        ).json

    @staticmethod
    def jsonify_all():
        table = FunctionsGroup.query.all()
        return jsonify([row.self_jsonify() for row in table])

##################################################
########### DBCONNECTION MODEL CLASS ####################
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
    

    def __init__(self, db_type, user, password, hostname, port, schema, name, conn_string):
        self.db_type = db_type
        self.schema = schema
        self.user = user
        self.password = password
        self.hostname = hostname
        self.port = port
        self.name = name
        self.conn_string = conn_string

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
    scenario_id = db.Column(db.Integer)
    ovr_file_location = db.Column(db.Text)
    db_conn_string = db.Column(db.Text)
    priority = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    message = db.Column(db.Text)

    def __init__(self, mission_id=None, mission_type=0, function_id=None,
                 run_id=None, scenario_id=None, ovr_file_location=None, db_conn_string=None,
                 priority=1, user_id=None, status=0, message=None):
        
        self.mission_id = mission_id
        self.mission_type = mission_type
        self.function_id = function_id
        self.run_id = run_id
        self.scenario_id = scenario_id
        self.ovr_file_location = ovr_file_location
        self.db_conn_string = db_conn_string
        self.priority = priority
        self.user_id = user_id
        self.status = status
        self.message = message
        
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
    
class Mission(db.Model):
    __tablename__ = 'Mission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name=None):
        if name:
            self.name=name
        else:
            self.name='mission'+str(self.id)
    
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
        if not type(runs) == type(list()):
            runs = [runs]
    
        conn = DbConnector(json_data['db_name'], 'postgres', 'dvirh', 'localhost', '5432', 'octopusdb')
        mission = Mission(json_data['mission_name'])
        db.session.add(mission)
        db.session.commit()
        user_id = json_data['user_id']
        for run in runs:
            for func in functions:
                task = Task(mission.id, conn, run, func.id, user_id)
                tasks_queue.put_nowait(task)
                # task.log()
                # task.run()
                # task.update()

class OverView(db.Model):
    __tablename__ = 'OverView'
    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer)
    overall_status = db.Column(db.Integer)
    # result_id = db.relationship('AnalyseResult', backref='OverView', lazy=True, uselist=True)
    elapsed_time = db.Column(db.Float)

    def __init__(self, mission_id, results, overall_status=None, result_id=[] , time_elapsed=None):
        self.mission_id = mission_id
        self.overall_status = overall_status
        # self.result_id = result_id
        self.time_elapsed = time_elapsed
        db.session.add(self)
        db.session.commit()
        for result in results:
            analyse_result = AnalyseResult(overview_id=self.id, run_id=result['run_id'], db_conn='db_conn',
                                           result_status=result['result_status'], 
                                           result_text=result['result_text'],
                                           result_array=result['result_arr'])#,
                                        #    result_array_header=[],#result['result_array_header'],
                                        #    result_array_types=[])#=result['result_array_types'])

            
                                           

class AnalyseResult(db.Model):
    __tablename__ = 'AnalyseResult'
    id = db.Column(db.Integer, primary_key=True)
    # overview_id = db.Column(db.Integer, db.ForeignKey('OverView.id'))
    task_id = db.Column(db.Integer)
    run_id = db.Column(db.Integer)
    db_conn = db.Column(db.Text)
    result_status = db.Column(db.Integer)
    result_text = db.Column(db.Text)
    result_array = db.relationship('ResultArray', backref='AnalyseResult', lazy=True, uselist=True)
    result_array_header = db.Column(db.Text)
    result_array_types = db.Column(db.Text)

    def __init__(self, task_id, run_id,  result_status, result_text,
                db_conn_string=None, result_array=None, result_array_header=None, result_array_types=None):
        self.task_id = task_id
        self.run_id = run_id
        self.db_conn = db_conn_string
        self.result_status = result_status
        self.result_text = result_text
        self.result_array = []
        self.result_array_types = result_array_types
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
                header = ''
                for col in cols:
                    header += col
                status = True
            else:
                message = 'result array must not have more than 30 columns'
        else:
            message = 'result array must be a DataFrame'
            
        return (status, message, header)
    
    def log(self, data_obj, error_queue):
        db.session.add(self)
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
        return message

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
    
    # @staticmethod
    # def log(result_id, result_array, data_obj, headers=None):
    #     result_array = ResultArray(result_id, data_obj, headers)

    
