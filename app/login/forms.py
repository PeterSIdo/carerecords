#C:\Users\Peter\Documents\Care-Home-4\app\login\forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    user_mode = SelectField('User Mode', choices=[
        ('c', 'Carer'), 
        ('m', 'Manager'), 
        ('f', 'Family'), 
        ('a', 'Admin')
    ], validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')