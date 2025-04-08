from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobAdditionForm(FlaskForm):
    teamleader = IntegerField('teamleader id', validators=[DataRequired()])
    job = StringField('job description', validators=[DataRequired()])
    work_size = IntegerField('work size (h)', validators=[DataRequired()])
    collaborators = StringField('collaborators (separated by commas)', validators=[DataRequired()])
    categories = StringField('categories (separated by commas)',
                                validators=[DataRequired()])
    is_finished = BooleanField('is finished')
    submit = SubmitField('Confirm')