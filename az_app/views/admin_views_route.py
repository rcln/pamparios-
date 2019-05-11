from flask import Flask, render_template, request, redirect, url_for, flash

from .forms_in_flask.admin.admin_flaskform import LoginForm, ServerUserCreateForm

from .forms_in_flask.admin.upload_extract_flaskform import UploadFileExtractTextForm, ExtractButton, ExtractedFilesForm

from .forms_in_flask.admin.add_language_flaskform import AddLanguage

from flask_bootstrap import Bootstrap

from ..controls import account_controler, language_controler, upload_controler
from ..controls.app_services import ocr_extraction, giza_translation_service

import os

from werkzeug.utils import secure_filename

from flask_login import LoginManager, login_required, logout_user, current_user, login_user

from ..models import adminUserModel, applicationModel

from PyPDF2 import PdfFileReader

'''
template_folder='../templates'  ===>>> The folder in which the templates (HTML Files ...) will be stored

static_folder="../app_ressources"  ===>>> The folder in which the scripts (JavaScript, CSS3 ...) and images will be stored
'''
mayapp = Flask(__name__, template_folder='../templates', static_folder="../app_ressources")

# The initialization of the application configuration
mayapp.config.from_object('az_app.controls.appconfig')
mayapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


Bootstrap(mayapp)

login_manager = LoginManager()
login_manager.init_app(mayapp)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return adminUserModel.AdminsAcount.query.get(int(user_id))


@mayapp.context_processor
def spread_user():

    try:
        return dict(fname=current_user.fname_admin, lname=current_user.lname_admin, umail=current_user.email_admin, all_lang=languages())

    except:

        return ''


"""
                                                            +-----------------------------------------+
                                                            +                                         +
                                                            +                                         +                                                            
                                                            +   +----------------------------------+  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +             HOME PAGES           +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +


"""


#  START OF THE INDEX PAGE OF THE ADMINISTRATION AND TRANSLATION PLATEFORM

@mayapp.route('/ocr/', methods=['GET', 'POST'])
@mayapp.route('/ocr/index/', methods=['GET', 'POST'])
@login_required
def index():
    """
        This view displays the index page of the administration's plateform
    """

    return render_template('carousel.html')


@mayapp.route('/', methods=['GET', 'POST'])
@mayapp.route('/home/', methods=['GET', 'POST'])
def home():
    """
        This view displays the index page of the translation's plateform
    """

    langus = language_controler.display_available_languages()

    return render_template('client_translator/home.html', langus=langus)

#  END OF THE INDEX PAGE OF THE ADMINISTRATION AND TRANSLATION PLATEFORM


"""
                                                            +-----------------------------------------+
                                                            +                                         +
                                                            +                                         +                                                            
                                                            +   +----------------------------------+  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +      TRANSLATION SERVICE VIEW    +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +


"""
@mayapp.route('/ocr/traduct/', methods=['POST'])
def translatorview():
    """
        This view calls the dedicated translation service in file "az_app/controls/app_services/giza_translation_service.py"
        and return the result of the translation
    """

    return giza_translation_service.translate(request.form.get('phrase'), request.form.get('prem_langu'), request.form.get('secon_langu'))






"""
                                                            +-----------------------------------------+
                                                            +                                         +
                                                            +                                         +                                                            
                                                            +   +----------------------------------+  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +      LOGIN AND LOGOUT VIEWS      +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +


"""


# =====================================================================================================================

@mayapp.route('/ocr/login/', methods=['GET', 'POST'])
def login():
    """
        This view allows to authenticate and to get access to the administration plateform
    """

    login_form = LoginForm()

    if login_form.validate_on_submit():

        request_value = account_controler.check_server_login(request.form.get('email'), request.form.get('pwd'))

        if request_value == 0:

            flash('The Account entered doesn\'t match', 'danger')

        else:

            login_user(request_value, remember=login_form.rmber.data)
            print(request_value)

            return redirect(url_for('index'))

    return render_template('login.html', form=login_form)


@mayapp.route('/ocr/logout/', methods=['GET', 'POST'])
def logout():
    """
        This view disconnects the user from the plateform
    """
    logout_user()
    return redirect(url_for('login'))

# =====================================================================================================================



"""
                                                            +-----------------------------------------+
                                                            +                                         +
                                                            +                                         +                                                            
                                                            +   +----------------------------------+  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +        APP SETTINGS VIEWS        +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +


"""


@mayapp.route('/ocr/adduser/', methods=['GET', 'POST'])
@login_required
def add_server_account():
    """
        This view implements the functionnality of creating new users for the plateform
    """

    server_account_form = ServerUserCreateForm()
    if server_account_form.validate_on_submit():

        if account_controler.create_server_user(request.form.get('ftname'), request.form.get('ltname'), request.form.get('email'), request.form.get('permission')):
            return redirect(url_for('show_users'))
        else:
            return redirect(url_for('show_us'))

    return render_template('admin_user_pages/add_server_user.html', form=server_account_form)


@mayapp.route('/ocr/addlang/', methods=['GET', 'POST'])
@login_required
def add_language():
    """
        This view implements the functionnality of creating new languages of translations
    """

    addlangform = AddLanguage()

    if addlangform.validate_on_submit():

        if language_controler.create_new_language(request.form.get('lang_name'), request.form.get('lang_desc')):
            return redirect(url_for('index'))
        else:
            return redirect(url_for('sfd'))

    return render_template('doc_translater_pages/add_languages.html', form=addlangform)


# =====================================================================================================================


"""
                                                            +-----------------------------------------+
                                                            +                                         +
                                                            +                                         +                                                            
                                                            +   +----------------------------------+  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +         DICTIONNARY VIEWS        +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +





"""


# =====================================================================================================================

@mayapp.route('/ocr/dictionary/', methods=['GET', 'POST'])
@login_required
def dictionary():
    """
        It is not yet implemented
        But displays a page with the words of a language and its transaltion in others language
    """

    return render_template('doc_translater_pages/dictionary.html')


@mayapp.route('/ocr/addtranslation/', methods=['GET', 'POST'])
@login_required
def add_translations():
    """"
        It is not yet implemented
        But allow to add new word in the dictionnary
    """
    return render_template('doc_translater_pages/add_translations.html')


@mayapp.route('/ocr/translate/', methods=['GET', 'POST'])
@login_required
def translate_not_translated():
    """
        It is not yet implemented
        But allows to correct the correct words which are not correctly recognized by the OCR Service
    """

    return render_template('doc_translater_pages/translate.html')


# =====================================================================================================================
def languages():
    """
        THis just returns the list of available languages of the platform
    """

    langs = language_controler.display_available_languages()

    return langs

# =====================================================================================================================


"""
                                                            +-----------------------------------------+
                                                            +                                         +
                                                            +                                         +                                                            
                                                            +   +----------------------------------+  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +      UPLOADING/SCANNING VIEWS    +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +





"""


# =====================================================================================================================

@mayapp.route('/ocr/upload/', methods=['GET', 'POST'])
@login_required
def scan_files():
    """
        This one returns the page which allows upload documents in 'PDF' format whose data will be used to train the
        future translation's service
    """

    upload_extract = UploadFileExtractTextForm()

    lang_list = [(i.id_lang, i.language) for i in applicationModel.LanguagesApp.query.all()]

    upload_extract.lang.choices = lang_list

    if upload_extract.validate_on_submit():

        print('Start')

        the_file = request.files['slctFile']

        the_file_name = secure_filename(the_file.filename)

        the_file.save(os.path.join(mayapp.config['UPLOAD_FOLDER'] + mayapp.config['UPLOADED_FILE_DIR'], the_file_name))

        file_reader = PdfFileReader(the_file)

        doc_number_of_pages = file_reader.numPages

        if int(request.form.get('strtPage')) > doc_number_of_pages or int(request.form.get('endPage')) > doc_number_of_pages:

            os.remove(os.path.join(mayapp.config['UPLOAD_FOLDER'] + mayapp.config['UPLOADED_FILE_DIR'], the_file_name))

            flash('You cannot exceed the file\'s number of pages ', 'danger')

        else:

            if int(request.form.get('strtPage')) < int(request.form.get('endPage')):

                if upload_controler.upload_document(the_file_name, current_user.id_admin, int(request.form.get('lang')), request.form.get('strtPage'), request.form.get('endPage'), doc_number_of_pages, the_file.read()):

                    flash('Document added Successfully !', 'success')

                    return redirect(url_for('view_files_uploaded'))

                else:

                    os.remove(os.path.join(mayapp.config['UPLOAD_FOLDER'] + mayapp.config['UPLOADED_FILE_DIR'], the_file_name))

                    flash('An Error occured when uploading file', 'danger')

            else:

                os.remove(os.path.join(mayapp.config['UPLOAD_FOLDER'] + mayapp.config['UPLOADED_FILE_DIR'], the_file_name))

                flash('The Start page cannot be higher than the End Page', 'danger')

    return render_template('doc_scanner_pages/upload.html', form=upload_extract)


@mayapp.route('/ocr/uploaded/', methods=['GET', 'POST'])
@login_required
def view_files_uploaded():
    """
        This view displays the documents uploaded through the platform
    """

    extract_button_form = ExtractButton()
    doc_uploaded = upload_controler.display_uploaded_docs()

    if extract_button_form.is_submitted():

        if ocr_extraction.create_respective_dir():

            if ocr_extraction.create_first_page_images():

                if ocr_extraction.transform_to_images():

                    if ocr_extraction.extract_words_from_images():

                        print('AH TOUT S\'EST BIEN PASSÉ')

                        return redirect(url_for('index'))

    return render_template('doc_scanner_pages/uploaded_files.html', docs=doc_uploaded, form=extract_button_form)


@mayapp.route('/ocr/extracting/', methods=['GET', 'POST'])
@login_required
def display_extracting_progress():
    """
        This displays a page with the cover page of all uploaded documents
    """

    doc_uploaded = upload_controler.display_uploaded_docs()

    document = ocr_extraction.show_cover_pages_name()

    if document is None:

        print('Nothing found Sorry')

    return render_template('doc_scanner_pages/extracting.html', cover_pages=document, docss=doc_uploaded)


@mayapp.route('/ocr/extracting/<filename>/', methods=['GET', 'POST'])
@login_required
def display_file_images_progression(filename):
    """
        This view is displayed on click of a cover page from the view '/ocr/extracting/'
        And it displays the documents images converted pages progression
    """

    document = ocr_extraction.show_cover_pages_name()

    f_images = ocr_extraction.show_each_file_pages_images(filename)

    return render_template('doc_scanner_pages/extracting.html', cover_pages=document, files_images=f_images)


@mayapp.route('/ocr/extracted/', methods=['GET', 'POST'])
@login_required
def display_extracted_pages_name():
    """
        It displays a page wich contains in a select the name of uploaded documents
    """

    extracted_files = ExtractedFilesForm()

    docs_name = applicationModel.DocumentAdded.query.all()

    return render_template('doc_scanner_pages/extracted.html', form=extracted_files, docs=docs_name)


@mayapp.route('/ocr/extracted/<filename>/', methods=['GET', 'POST'])
@login_required
def display_spec_extr_page_nums(filename):
    """
        It displays a page wich contains in a select the name of uploaded documents
        And its extracted pages number
    """

    extracted_files = ExtractedFilesForm()

    name_pdf_extension = filename + '.pdf'

    file_pages = applicationModel.DocumentAdded.query.filter_by(name_doc=name_pdf_extension).first()

    docs_name = applicationModel.DocumentAdded.query.all()

    return render_template('doc_scanner_pages/extracted.html', form=extracted_files, strt_page=file_pages.scan_start_doc, end_page=file_pages.scan_end_doc, docs=docs_name, name_of_file=filename)


@mayapp.route('/ocr/extracted/<filename>/<numpage>/', methods=['GET', 'POST'])
@login_required
def display_file_and_extracted_pages(filename, numpage):
    """
        It displays a page wich contains in a select the name of uploaded documents, its extracted pages number
        And on select of a page, it displays the image of the page and the extracted text from this page(which
        is editable)
    """

    extracted_files = ExtractedFilesForm()

    name_pdf_extension = filename + '.pdf'

    file_pages = applicationModel.DocumentAdded.query.filter_by(name_doc=name_pdf_extension).first()

    docs_name = applicationModel.DocumentAdded.query.all()

    page_image = '/app_ressources/translator_ressources/converted_files/' + filename + '/' + filename + '__page_' + numpage + '.jpg'
    page_text_path = 'az_app/app_ressources/translator_ressources/txt_extracted_files/' + filename + '/' + filename + '__page_' + numpage + '.txt'
    page_text = open(page_text_path, 'r').read()

    if request.method == 'POST':

        page_text_opened = open(page_text_path, 'w+')
        page_text_opened.write(request.form['text_to_correct'])
        print('CHANGES ARE MADE!!!!!!!!')

    return render_template('doc_scanner_pages/extracted.html', form=extracted_files, strt_page=file_pages.scan_start_doc, end_page=file_pages.scan_end_doc, page_image=page_image, page_text=page_text, docs=docs_name, name_of_file=filename)


# =====================================================================================================================


"""
                                                            +-----------------------------------------+
                                                            +                                         +
                                                            +                                         +                                                            
                                                            +   +----------------------------------+  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +   LES PAGES D'AFFICHAGES DES     +  +
                                                            +   +            UTILISATEURS          +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +





"""

# =====================================================================================================================


@mayapp.route('/ocr/users/', methods=['GET', 'POST'])
@login_required
def show_users():
    """
        Here is the view which display the users of the administration platform
    """

    all_users = account_controler.display_server_users()

    for us in all_users:

        print(us.fname_admin)

    return render_template('admin_user_pages/users_list.html', users=all_users)

# =====================================================================================================================


@mayapp.route('/ocr/surfers/', methods=['GET', 'POST'])
@login_required
def show_surfers():
    """
        This view is not implemented, but should display just the account of the surfer(users which use the translation
        platform and have an account
    """

    return render_template('surfer_user_pages/surfer_list.html')

# =====================================================================================================================
