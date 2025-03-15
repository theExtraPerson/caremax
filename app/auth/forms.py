from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User
from wtforms import ValidationError

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')

#Registration Form
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
    DataRequired(),
    Length(1, 64),
    Regexp(r'^[A-Za-z\s\'-]+$', 0, 
           'Names can only contain letters, spaces, hyphens, and apostrophes.')
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message='Passwords must match!')])
    location = StringField('Location', validators=[DataRequired()])
    role = SelectField('Role', choices=[
        ('user', 'User'),
        ('admin', 'Administrator'),
        ('sequencer', 'Sequencer'),
        ('clinician', 'Clinician'),
        ('researcher', 'Researcher')
    ], validators=[DataRequired()])
    submit = SubmitField('Register')

    def valdate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already used.')
    
