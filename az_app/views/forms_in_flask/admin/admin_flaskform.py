from flask_wtf import *

from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, BooleanField

from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterAdmin(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    register = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    pwd = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=14)])
    rmber = BooleanField('Remember me')
    login = SubmitField('Login')


class ServerUserCreateForm(FlaskForm):
    ftname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    ltname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    permission = SelectField('Permission', validators=[DataRequired()], choices=[('0', 'Grant...'), ('1', 'Ordinary'), ('2', 'Administrator')])
    create = SubmitField('Create')
