from flask_wtf import *
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddLanguage(FlaskForm):
    lang_name = StringField('Language', validators=[DataRequired(), Length(min=2, max=50)])
    lang_desc = TextAreaField('Brief Description', validators=[DataRequired(), Length(min=4, max=200)])
    addbutton = SubmitField('Insertion')
