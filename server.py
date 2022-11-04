# SERVER.PY

# SETUP
#########################################################################

# Flask > render_template > render template file based on the Jinja2 from file templates folder
# Flask > redirect > redirect users to a specified URL
# Flask > url_for > build and generate URLs
from flask import Flask, render_template, redirect, url_for

# forms.py > Classes to outline the Form options
from forms import TeamForm, ProjectForm

# model.py > User > a Class defining the SQL table users
# model.py > connect_to_db > connection to the PostGreSQl Database
from model import db, User, Team, Project, connect_to_db

# Name of the location in which app is defined
app = Flask(__name__)

# Verify legitimate cookie ownership
app.secret_key = "keep this secret"

# A Place holder for the first index user_id "House Stark"
user_id = 1

# ROUTES
#########################################################################

# Render html page "home"
@app.route("/")
def home():
    team_form = TeamForm()
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)
    return render_template("home.html", team_form = team_form, project_form = project_form)

# Team View Function > html page "home"
@app.route("/add-team", methods=["POST"])
def add_team():
    team_form = TeamForm()

    if team_form.validate_on_submit():
        team_name = team_form.team_name.data
        new_team = Team(team_name, user_id)
        db.session.add(new_team)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

# Project View Function > html page "home"
@app.route("/add-project", methods=["POST"])
def add_project():
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)

    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        description = project_form.description.data
        completed = project_form.completed.data
        team_id = project_form.team_selection.data

        new_project = Project(project_name, completed, team_id, description = description)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

# EXECUTE 
#########################################################################

# Run code... python server.py
# Launch... http://localhost:7032

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, port=7032, host="localhost")