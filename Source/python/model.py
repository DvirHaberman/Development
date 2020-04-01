##################################################################################################
### This model defines the ORM model classes inheriting from flask_sqlalchemy db.Model         ###
### The classes contains one-to-one, one-to-man and many-to-many relationships                 ###
### It is advised to have a firm knowledge of these relationships before committing any changes ###
##################################################################################################


import pandas as pd
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, request, jsonify, render_template
import json
from datetime import datetime
from time import time, sleep
from threading import Thread
from queue import Queue
import importlib
import sys

db = SQLAlchemy()

tasks_queue = Queue()

FunctionsAndGroups = db.Table('FunctionsAndGroups',
                              db.Column('function_id', db.Integer,
                                        db.ForeignKey('OctopusFunctions.id')),
                              db.Column('group_id', db.Integer,
                                        db.ForeignKey('FunctionsGroup.id'))
                              )


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

    def __repr__(self):
        print(f'my name is {self.name} and my function are:')
        for func in self.functions:
            print(func.printme())

    def printme(self):
        str1 = f'my name is {self.name} and my function are:'
        for func in self.Functions:
            str1 = str1 + func.printme()
        return str1


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


#####################################################
########### OCTOPUSFUNCTIONS MODEL CLASS ############
#####################################################


class OctopusFunction(db.Model):
    __tablename__ = "OctopusFunctions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    callback = db.Column(db.Text)
    location = db.Column(db.Text)
    owner = db.Column(db.Integer, db.ForeignKey('Users.id'))
    status = db.Column(db.Integer)
    tree = db.relationship(
        'Trees', backref='OctopusFunction', lazy=True, uselist=False)
    kind = db.Column(db.Text)
    tags = db.Column(db.Text)
    description = db.Column(db.Text)
    # project = db.Column(db.Integer, db.ForeignKey('Project.id'))
    version = db.Column(db.Integer)
    version_comments = db.Column(db.Text)
    function_checksum = db.Column(db.Text)
    handler_checksum = db.Column(db.Text)
    changed_date = db.Column(db.DateTime)
    is_locked = db.Column(db.Integer)
    function_parameters = db.relationship(
        'FunctionParameters', backref='OctopusFunction', lazy=True, uselist=True)

    def __init__(self, name=None, callback=None, location=None, owner=None, status=None, tree=None,
                 kind=None, tags=None, description=None, version_comments=None,  # project=None,
                 function_checksum=None, version=None, handler_checksum=None, function_parameters=[], changed_date=None, is_locked=0):
        self.name = name
        self.callback = callback
        self.location = location
        self.owner = owner
        self.status = status
        self.tree = tree
        self.kind = kind
        self.tags = tags
        self.description = description
        # self.project = project
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
            name=self.name,
            callback=self.callback,
            location=self.location,
            owner=owner,
            status=self.status,
            tree=tree,
            kind=self.kind,
            tags=self.tags,
            description=self.description,
            groups=groups,
            version=self.version,
            version_comments=self.version_comments,
            function_checksum=self.function_checksum,
            handler_checksum=self.handler_checksum,
            changed_date=self.changed_date,
            is_locked=self.is_locked,
            function_parameters=jsonify(
                [param.self_jsonify() for param in self.function_parameters]).json

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

    def run_dummy(self, db_conn, run_id):
        return {status:(self.id % 5), text:'man that was a long run...', result_arr : None}

    def __repr__(self):
        print(f'my name is {self.name} and my owner is {self.owner}')

    def printme(self):
        return f'my name is {self.name} and my owner is {self.owner}'

    # def push(self, DB_Connection, run_id):
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
########### TASK MODEL CLASS ####################
##################################################


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

    def __init__(self, mission_id=None, mission_type='function', function_id=None,
                 run_id=None, scenario_id=None, ovr_file_location=None, db_conn_string=None,
                 priority=None, user_id=None, status=0):
        
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
    

# class OverView(db.Model):

#     def __init__(self, mission_id, task_id, status, time_elapsed):