from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=10)])
    user_password = PasswordField('Password', validators=[DataRequired(), Length(max=20)])
    user_name = StringField('Full Name', validators=[DataRequired(), Length(max=10)])
    user_age = IntegerField('Age', validators=[DataRequired()])
    user_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add User')
