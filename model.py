# MODEL.PY


# SETUP CONFIGURATION
#########################################################################
# Flask SLQAlchemy Instance #

# Importing the operating system
import os

# Importing flask sqlalchemy to the page
from flask_sqlalchemy import SQLAlchemy

# Instatiate SQLAlchemy and save to the variable db
db = SQLAlchemy()


# CLASS/TABLE CONFIGURATION
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
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    
# Teams(s) Class/Table
class Team(db.Model):

    # Override to set SQL table name
    __tablename__ = "teams"
    
    # Data-types and Arguments for the SQL table
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    team_name = db.Column(db.String(255), unique = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

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
    
    def __init__(self, project_name, completed, team_id, **kwargs):
        self.project_name = project_name
        self.completed = completed
        self.team_id = team_id

        if "description" in kwargs:
            self.description = kwargs["description"]



# CONNECTION CONFIGURATION
#########################################################################
# Allowing file to configure database
def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    

# EXECUTE CONFIGURATION
#########################################################################
# Run code
if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to db...")