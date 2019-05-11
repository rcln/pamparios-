
from flask_wtf import *
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.widgets.html5 import *
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, BooleanField, FileField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, NumberRange

# from .. .. controls
from az_app.controls import language_controler
from az_app.models.applicationModel import LanguagesApp


# def get_pk(obj):
#     return repr(obj)

# lang_list = [(i.id_lang, i.language) for i in LanguagesApp.query.all()]


class UploadFileExtractTextForm(FlaskForm):
    slctFile = FileField('Choose Files', validators=[FileRequired('PDF File is required'), FileAllowed(['pdf'], 'Only PDF File are allowed')])
    strtPage = IntegerField('Start Page', validators=[DataRequired(), NumberRange(min=1)], widget=NumberInput())
    endPage = IntegerField('End Page', validators=[DataRequired(), NumberRange(min=1)], widget=NumberInput())
    # lang = SelectField('Permission', validators=[DataRequired()], choices=[(language_controler.display_available_languages().id_lang, language_controler.display_available_languages().language) for langus in language_controler.display_available_languages()])
    # lang = QuerySelectField('Permission', validators=[DataRequired()], query_factory=language_controler.display_available_languages)
    # lang = QuerySelectField('Language', query_factory=language_controler.display_available_languages, get_pk=get_pk)
    lang = SelectField('Languages', validators=[DataRequired()], coerce=int)
    start = SubmitField('Start')


class ExtractButton(FlaskForm):

    extract = SubmitField('Extract Text')


class ExtractedFilesForm(FlaskForm):

    files_name = SelectField('Select the file', validators=[DataRequired()], coerce=int)
    files_pages = SelectField('Choose a page', validators=[DataRequired()], coerce=int)
