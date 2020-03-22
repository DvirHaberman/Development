##################################################################################################
### This model defines the ORM model classes inheriting from flask_sqlalchemy db.Model         ###
### The classes contains one-to-one, one-to-man and many-to-many relationships                 ###
### It is advised to have a firm knowledge of these relationships before commitind any changes ###
##################################################################################################


import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, request, jsonify, render_template
import json
from datetime import datetime


db = SQLAlchemy()

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
            name = self.name,
            users = jsonify([user.self_jsonify() for user in self.users]).json
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
            name = self.name,
            users = jsonify([user.self_jsonify() for user in self.users]).json
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
    project =  db.Column(db.Integer, db.ForeignKey('Project.id'))

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


# UsersProjects = db.Table('UsersProjects',
#                           db.Column('user_id', db.Integer, db.ForeignKey('Users.id'), primary_key=True),
#                           db.Column('project_id', db.Integer, db.ForeignKey('Project.id'), primary_key=True)
#                         )

    def self_jsonify(self):
        return jsonify(
            name = self.name,
            first_name = self.first_name,
            last_name = self.last_name,
            password_sha = self.password_sha,
            state = self.state,
            role = self.Role.query.get(self.role).name,
            team = self.Team.query.get(self.team).name,
            functions = jsonify([func.self_jsonify() for func in self.functions]).json,
            max_priority = self.max_priority,
            project = Project.query.get(self.project).name
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
            name = self.name,
            version = self.version,
            users = jsonify([user.self_jsonify() for user in self.users]).json
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
            function_id = self.function_id,
            kind = self.kind,
            value = self.value,
            type = self.type
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
        'TreeStructre', backref='OctopusFunction', lazy=True, uselist=False)
    kind = db.Column(db.Integer)
    tags = db.Column(db.Text)
    description = db.Column(db.Text)
    # project = db.Column(db.Integer, db.ForeignKey('Project.id'))
    version = db.Column(db.Integer)
    version_comments = db.Column(db.Text)
    function_checksum = db.Column(db.Text)
    handler_checksum = db.Column(db.Text)
    changed_date = db.Column(db.DateTime)
    is_locked = db.Column(db.Integer)
    function_parameters  = db.relationship('FunctionParameters', backref='OctopusFunction', lazy=True, uselist=True)

    def __init__(self, name=None, callback=None, location=None, owner=None, status=None, tree=None,
                 kind=None, tags=None, description=None, version_comments=None, #project=None,
                 function_checksum=None, version=None, handler_checksum=None, function_parameters=[], changed_date=datetime.utcnow(), is_locked=0):
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
        return jsonify(
            name=self.name,
            callback=self.callback,
            location=self.location,
            owner=User.query.get(self.owner).name,
            status=self.status,
            tree=self.tree,
            kind=self.kind,
            tags=self.tags,
            description=self.description,
            # project=self.project,
            version=self.version,
            version_comments=self.version_comments,
            function_checksum=self.function_checksum,
            handler_checksum=self.handler_checksum,
            changed_date=self.changed_date,
            is_locked=self.is_locked,
            function_parameters =  jsonify([param.self_jsonify() for param in self.function_parameters]).json

        ).json

    @staticmethod
    def save_function(data):
        data = json.loads(data)
        func = OctopusFunction(
                name=data.name,
                callback=data.callback,
                location=data.location,
                owner=data.owner,
                status=data.status,
                # tree=row.tree,
                kind=data.kind,
                tags=data.tags,
                description=data.description,
                # project=row.project,
                version=data.version,
                version_comments=data.version_comments,
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

    def __repr__(self):
        print(f'my name is {self.name} and my owner is {self.owner}')

    def printme(self):
        return f'my name is {self.name} and my owner is {self.owner}'




###############################################
########### TREENODES MODEL CLASS ############
###############################################

class TreeNodes(db.Model):
    # __tablename__ = "Trees"
    id = db.Column(db.Integer, primary_key=True)
    function = db.Column(db.Integer, db.ForeignKey('OctopusFunctions.id'))
    node = db.Column(db.Integer)
    description = db.Column(db.Text)
    alias = db.Column(db.Text)



##################################################
########### TREESTRUCTURE MODEL CLASS ############
##################################################

class TreeStructre(db.Model):
    # __tablename__ = "Trees"
    id = db.Column(db.Integer, primary_key=True)
    function = db.Column(db.Integer, db.ForeignKey('OctopusFunctions.id'))
    parent = db.Column(db.Integer)
    children = db.Column(db.Text)
    node = db.Column(db.Integer)
