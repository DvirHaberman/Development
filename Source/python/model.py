from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///OctopusDB.db"
    return app

class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

class OctopusFunction(db.Model):
    __tablename__ = "OctopusFunctions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    callback = db.Column(db.Text)
    location = db.Column(db.Text)
    # owner = db.relationship('User', backref='OctopusFunction', lazy=True)
    status = db.Column(db.Integer)
    # tree = db.relationship('Tree', backref='OctopusFunction', lazy=True, uselist=False)
    kind = db.Column(db.Integer)
    Tags = db.Column(db.Text)
    description = db.Column(db.Text)
    # Project = db.relationship('Project', backref='OctopusFunction', lazy=True, uselist=False)
    version_comments = db.Column(db.Text)

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

# if __name__ == "__main__":