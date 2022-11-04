# MODEL.PY

# SETUP
#########################################################################

# operating system > environ > mapping objects in PostgreSQL
from os import environ

# flask sqlalchemy > SQLAlchemy > converts Pythonic SQLAlchemy Expression Language to SQL statements
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy > db > create object once and will attach as needed to a Flask application
db = SQLAlchemy()

# CLASS/SQL-TABLE
#########################################################################

# User(s) Class/Table
class User(db.Model):

    # Override to set SQL table name
    __tablename__ = "users"

    # Data-types and Arguments for the SQL table
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    
    teams = db.relationship("Team", backref = "user", lazy = True)
    
    # Instances for users login
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    # (Instances for teams)
    def get_all_projects(self):
        projects = []

        for team in self.teams:
            for project in team.projects:
                projects.append(project)

        return projects
    
# Teams(s) Class/Table
class Team(db.Model):

    # Override to set SQL table name
    __tablename__ = "teams"
    
    # Data-types and Arguments for the SQL table
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    team_name = db.Column(db.String(255), unique = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    # Instances for team linked to user
    def __init__(self, team_name, user_id):
        self.team_name = team_name
        self.user_id = user_id

# Project(s) Class/Table
class Project(db.Model):

    # Override to set SQL table name
    __tablename__ = "projects"

    # Data-types and Arguments for the SQL table
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    project_name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = True)
    completed = db.Column(db.Boolean, default = False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable = False)
    
    # Instances for porject linked to user
    def __init__(self, project_name, completed, team_id, **kwargs):
        self.project_name = project_name
        self.completed = completed
        self.team_id = team_id

        # Key Word Argument to allow description as an optional instance
        if "description" in kwargs:
            self.description = kwargs["description"]

# CONNECTION
#########################################################################

# Allowing file to configure to the database
def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    
# EXECUTE
#########################################################################

# Imported by the server.py
if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to db...")