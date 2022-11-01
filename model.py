# Flask SLQAlchemy Instance

# Importing the operating system
import os

# Importing flask sqlalchemy to the page
from flask_sqlalchemy import SQLAlchemy


# Instatiate SQLAlchemy and save to the variable db
db = SQLAlchemy()

# Classes holding sqlalchemy syntax to genrate SQL data model


# User(s) Table/Class
class User(db.Model):

    # Name override to set SQL table name
    __tablename__ = "users"

    # Data-types and Arguments for the SQL table
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    
    
# Teams(s) Table/Class
class Team(db.Model):

    # Name override to set SQL table name
    __tablename__ = "teams"
    
    # Data-types and Arguments for the SQL table
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    team_name = db.Column(db.String(255), unique = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)


# Project(s) Table/Class
class Project(db.Model):

    # Name override to set SQL table name
    __tablename__ = "projects"

    # Data-types and Arguments for the SQL table
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    project_name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = True)
    completed = db.Column(db.Boolean, default = False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable = False)
    

# Allow parameter app
def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    

# Run code
if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to db...")