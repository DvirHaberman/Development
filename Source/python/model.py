import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, request, jsonify, render_template
import json
from datetime import datetime


db = SQLAlchemy()


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', backref='Team', lazy=True, uselist=True)
    team_name = db.Column(db.Text)

    def __init__(self, team_name=None, users=[])
        self.team_name = team_name
        self.users = users

    def jsonify_all():
        return jsonify(
            name = self.name,
            functions = jsonify([user.self_jsonify() for user in self.users]).json
        ).json

class role(db.Model):



class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    password_sha = db.Column(db.Text)
    role = db.Column(db.Integer, db.ForeignKey('Role.id'))
    team = db.relationship('Team', backref='User', lazy=True)
    functions = db.relationship('OctopusFunction', backref='User', lazy=True)
    max_priority = db.Column(db.Integer)
    state = db.Column(db.Integer)
    projects = db.relationship('Project', secondary='UsersProjects', backref='User', lazy=True)
    def __init__(self, name=None, functions=[]):
        self.name = name
        self.functions = functions

UsersProjects = db.Table('UsersProjects', 
                          db.Column('user_id', db.Integer, db.ForeignKey('Users.id'), primary_key=True),
                          db.Column('project_id', db.Integer, db.ForeignKey('Project.id'), primary_key=True)
                        )

    def self_jsonify(self):
        return jsonify(
            name = self.name,
            functions = jsonify([func.self_jsonify() for func in self.functions]).json
            team = 
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

class Project(db.Model):
    __tablename__ = 'Project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    functions = db.relationship('OctopusFunction', backref='Project', lazy=True, uselist=True)
    version = db.Column(db.Text)

    def __init__(self, name=None, functions=None, version=None):
        self.name = name
        self.functions = functions
        self.version = version

    def self_jsonify(self):
        return jsonify(
            name = self.name,
            functions = self.functions,
            version = self.version
            ).json

class OctopusFunction(db.Model):
    __tablename__ = "OctopusFunctions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    callback = db.Column(db.Text)
    location = db.Column(db.Text)
    owner = db.Column(db.Integer, db.ForeignKey('Users.id'))
    status = db.Column(db.Integer)
    tree = db.relationship(
        'Tree_Structre', backref='OctopusFunction', lazy=True, uselist=False)
    kind = db.Column(db.Integer)
    tags = db.Column(db.Text)
    description = db.Column(db.Text)
    project = db.Column(db.Integer, db.ForeignKey('Project.id'))
    version = db.Column(db.Integer)
    version_comments = db.Column(db.Text)
    function_checksum = db.Column(db.Text)
    handler_checksum = db.Column(db.Text)
    changed_date = db.Column(db.DateTime)
    is_locked = db.Column(db.Integer)

    def __init__(self, name=None, callback=None, location=None, owner=None, status=None, tree=None,
                 kind=None, tags=None, description=None, project=None, version_comments=None,
                 function_checksum=None, version=None, handler_checksum=None, changed_date=datetime.utcnow(), is_locked=0):
        self.name = name
        self.callback = callback
        self.location = location
        self.owner = owner
        self.status = status
        self.tree = tree
        self.kind = kind
        self.tags = tags
        self.description = description
        self.project = project
        self.version = version
        self.version_comments = version_comments
        self.function_checksum = function_checksum
        self.handler_checksum = handler_checksum
        self.changed_date = changed_date
        self.is_locked = is_locked

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
            project=self.project,
            version=self.version,
            version_comments=self.version_comments,
            function_checksum=self.function_checksum,
            handler_checksum=self.handler_checksum,
            changed_date=self.changed_date,
            is_locked=self.is_locked
        ).json


    @staticmethod
    def jsonify_all():
        table = OctopusFunction.query.all()
        return jsonify([row.self_jsonify() for row in table])

    @staticmethod
    def return_all():
        return OctopusFunction.jsonify_all()

    def __repr__(self):
        print(f'my name is {self.name} and my owner is {self.owner}')

    def printme(self):
        return f'my name is {self.name} and my owner is {self.owner}'


class Tree_Nodes(db.Model):
    # __tablename__ = "Trees"
    id = db.Column(db.Integer, primary_key=True)
    function = db.Column(db.Integer, db.ForeignKey('OctopusFunctions.id'))
    node = db.Column(db.Integer)
    description = db.Column(db.Text)
    alias = db.Column(db.Text)


class Tree_Structre(db.Model):
    # __tablename__ = "Trees"
    id = db.Column(db.Integer, primary_key=True)
    function = db.Column(db.Integer, db.ForeignKey('OctopusFunctions.id'))
    parent = db.Column(db.Integer)
    children = db.Column(db.Text)
    node = db.Column(db.Integer)


class OctopusUtils:

    @staticmethod
    def get_all_functions():
        functions = OctopusFunction.query.all()
        # owner_id = functions[0].owner
        # owner = User.query.get(owner_id).name
        return jsonify(names=[func.name for func in functions])#, owners=owner)


class Jsonifer:

    @staticmethod
    def jsonify_list(list_to_jsonify):
        return jsonify(list_to_jsonify)


# class Owner(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Text)


class DataCollector():

    def __init__(self, source_file):
        self.file_handler = pd.ExcelFile(source_file)
    
    def CollectAll(self):
        self.get_functions()
        # self.get_projects()
        self.get_users()
        # self.get_trees()
    
    def get_functions(self):
        df = pd.read_excel(self.file_handler, 'Functions')
        try:
            for index, row in df.iterrows():
                func = OctopusFunction(
                    name=row.func_name,
                    callback=row.callback,
                    location=row.location,
                    owner=row.owner,
                    status=row.status,
                    # tree=row.tree,
                    kind=row.kind,
                    tags=row.tags,
                    description=row.description,
                    # project=row.project,
                    version=row.version,
                    version_comments=row.version_comments,
                    function_checksum=row.function_checksum,
                    handler_checksum=row.handler_checksum,
                    is_locked=row.is_locked
                )
                db.session.add(func)
            db.session.commit()
        except():
            print('problem in DataCollector - something went wrong with creating the functions table')

        
    def get_projects(self):
        df = pd.read_excel(self.file_handler, 'Projects')
        try:
            for index, row in df.iterrows():
                project = Project(
                    name = row.name,
                    functions = row.functions,
                    version = row.version
                )
                db.session.add(project)
            db.session.commit()
        except():
            print('problem in DataCollector - something went wrong with creating the projects table')

    
    def get_users(self):
        df = pd.read_excel(self.file_handler, 'Users')
        try:
            for index, row in df.iterrows():
                user = User(
                    name = row.user_name,
                    # functions = row.functions,
                )
                db.session.add(user)
            db.session.commit()
        except():
            print('problem in DataCollector - something went wrong with creating the users table')
        
