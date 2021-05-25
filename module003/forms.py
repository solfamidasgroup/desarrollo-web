from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectField, HiddenField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length
from wtforms.fields.html5 import DateField, TimeField, DateTimeLocalField
import datetime


class AssignmentCreateForm(FlaskForm):
    title = StringField('Assignment title',validators=[Length(max=50)])
    description = TextAreaField('Task Description')
    course_id = SelectField('Course (must create a library first)', choices = [], validators = [InputRequired()])
    date_expire = DateField('Choose an expiring date',format='%Y-%m-%d', default=datetime.datetime.today)
    time_expire = TimeField('Expiring time',format='%H:%M', default=datetime.time(23, 59))

class GradeForm(FlaskForm):
    grade = StringField('Update Grade',validators=[Length(max=50)])