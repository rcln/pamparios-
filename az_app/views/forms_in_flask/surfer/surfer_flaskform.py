from flask_wtf import *
from flask_admin.form import widgets
from wtforms.widgets import html5
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterSurfer(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    passwd_1 = PasswordField('Password', validators=[DataRequired(), Email()])
    passwd_2 = PasswordField('Confirm Your Password', validators=[DataRequired(), Email(), EqualTo('passwd_1')])
    register = SubmitField('Register')
