# FORMS.PY

# SETUP
#########################################################################

# flask-wtf > FlaskForm > implementing the fields in the template and handling the data
from flask_wtf import FlaskForm

# wtforms > Allows for options for each submit field
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField

# wtforms > validators > DataRequired > Verifies the form field is filled
# wtforms > validators > Length > Constrains the minimum and maximum input of the field
from wtforms.validators import DataRequired, Length

# CLASSES
#########################################################################

# Form to submit a team name
class TeamForm(FlaskForm):
    team_name = StringField('team name', validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField("submit")

# Form to submit a project name
class ProjectForm(FlaskForm):
    project_name = StringField('project name', validators=[DataRequired(), Length(min=4, max=255)])
    description = TextAreaField('description')
    completed = BooleanField("completed?")
    team_selection = SelectField("team")
    submit = SubmitField("submit")

    def update_teams(self, teams):
        self.team_selection.choices = [ (team.id, team.team_name) for team in teams ]
        
# EXECUTE
#########################################################################

# Imported into server.py