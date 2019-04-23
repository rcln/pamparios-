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


mayapp = Flask(__name__, template_folder='../templates', static_folder="../app_ressources")


mayapp.config.from_object('az_app.controls.appconfig')
mayapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


Bootstrap(mayapp)

login_manager = LoginManager()
login_manager.init_app(mayapp)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return adminUserModel.AdminsAcount.query.get(int(user_id))


"""
                                                            +-----------------------------------------+
                                                            +                                         +
                                                            +                                         +                                                            
                                                            +   +----------------------------------+  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +        PAGE INDEX/ACCUEIL        +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +


"""


#  DEBUT DE LA PAGE INDEX

@mayapp.context_processor
def spread_user():

    try:
        return dict(fname=current_user.fname_admin, lname=current_user.lname_admin, umail=current_user.email_admin, all_lang=languages())

    except:

        return ''


@mayapp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """
        Cette vue affiche la page languages.html, c'est une page simple qui affiche un popup des langues de traduction utilisées
    """

    return render_template('carousel.html')


#  FIN DE LA PAGE INDEX



"""
                                                            +-----------------------------------------+
                                                            +                                         +
                                                            +                                         +                                                            
                                                            +   +----------------------------------+  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +   LES PAGES DU MENU CONNEXION    +  +
                                                            +   +      ET CREATION DE COMPTE       +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +


"""


#  DEBUT DES VUES POUR LES COMPTES DE L'APPLICATION SERVEUR PAMPARIOS

@mayapp.route('/login/', methods=['GET', 'POST'])
def login():
    """
                Cette vue affiche la page login.html, c'est la page qui permet de s'authentifier avant d'acceder à
                l'application
    """

    login_form = LoginForm()

    if login_form.validate_on_submit():

        request_value = account_controler.check_server_login(request.form.get('email'), request.form.get('pwd'))

        if request_value == 0:
            # return redirect(url_for('dd'))
            flash('The Account entered doesn\'t match', 'danger')

        else:

            login_user(request_value, remember=login_form.rmber.data)
            print(request_value)

            return redirect(url_for('index'))

    return render_template('login.html', form=login_form)


@mayapp.route('/logout/', methods=['GET', 'POST'])
def logout():

    logout_user()
    return redirect(url_for('login'))


@mayapp.route('/adduser/', methods=['GET', 'POST'])
@login_required
def add_server_account():
    """
                Cette vue affiche la page login.html, c'est la page qui permet de s'authentifier avant d'acceder à
                l'application
    """

    server_account_form = ServerUserCreateForm()
    if server_account_form.validate_on_submit():

        if account_controler.create_server_user(request.form.get('ftname'), request.form.get('ltname'), request.form.get('email'), request.form.get('permission')):
            return redirect(url_for('show_users'))
        else:
            return redirect(url_for('show_us'))

    return render_template('admin_user_pages/add_server_user.html', form=server_account_form)


@mayapp.route('/addlang/', methods=['GET', 'POST'])
@login_required
def add_language():
    """
        Cette vue affiche la page languages.html, c'est une page simple qui affiche un popup des langues de traduction utilisées
    """

    addlangform = AddLanguage()

    if addlangform.validate_on_submit():

        if language_controler.create_new_language(request.form.get('lang_name'), request.form.get('lang_desc')):
            return redirect(url_for('index'))
        else:
            return redirect(url_for('sfd'))

        # print(ll)

        # if language_controler.create_new_language('sadfasd', 'desc1'):
        #     return redirect(url_for('index'))

    return render_template('doc_translater_pages/add_languages.html', form=addlangform)


#  FIN DES VUES POUR LES COMPTES DE A L'APPLICATION SERVEUR PAMPARIOS


"""
                                                            +-----------------------------------------+
                                                            +                                         +
                                                            +                                         +                                                            
                                                            +   +----------------------------------+  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +   LES PAGES DU MENU TRADUCTION   +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +





"""


#  DEBUT DES VUES POUR LA TRADUCTION

@mayapp.route('/dictionary/', methods=['GET', 'POST'])
@login_required
def dictionary():
    """
                Cette vue affiche la page dictionary.html, c'est une page simple qui permet de visualiser les mots qui
                ont été traduits
    """

    return render_template('doc_translater_pages/dictionary.html')


@mayapp.route('/addtranslation/', methods=['GET', 'POST'])
@login_required
def add_translations():
    """
            Cette vue affiche la page add_transaltions.html, qui permet d'ajouter de nouveaux pour une langue et de donner son
            équivalent pour la seconde langue
    """
    return render_template('doc_translater_pages/add_translations.html')


@mayapp.route('/translate/', methods=['GET', 'POST'])
@login_required
def translate_not_translated():
    """
        Cette vue affiche la page translate.html, qui permet de traduire manuellement certains mots qui n'ont pas été
        automatiquement traduit par le service de traduction
    """

    return render_template('doc_translater_pages/translate.html')

@login_required
def languages():
    """
        Cette vue affiche la page languages.html, c'est une page simple qui affiche un popup des langues de traduction utilisées
    """

    langs = language_controler.display_available_languages()

    # for lang in langs:
    #
    #     print('')
        # print(lang.language)

    return langs

#  FIN DES VUES POUR LA TRADUCTION


"""
                                                            +-----------------------------------------+
                                                            +                                         +
                                                            +                                         +                                                            
                                                            +   +----------------------------------+  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +   LES PAGES DU MENU IMPORTATION  +  +
                                                            +   +             DE FICHIERS          +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +
                                                            +   +                                  +  +





"""


# DEBUT DES VUES POUR LE SCAN DES FICHIERS

@mayapp.route('/upload/', methods=['GET', 'POST'])
@login_required
def scan_files():
    """
        Cette vue affiche la page languages.html, c'est une page simple qui affiche un popup des langues de traduction utilisées
    """

    upload_extract = UploadFileExtractTextForm()

    lang_list = [(i.id_lang, i.language) for i in applicationModel.LanguagesApp.query.all()]

    upload_extract.lang.choices = lang_list

    if upload_extract.validate_on_submit():

        print('DEBUUT')

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


@mayapp.route('/uploaded/', methods=['GET', 'POST'])
@login_required
def view_files_uploaded():
    """
        Cette vue affiche la page languages.html, c'est une page qui affiche les fichiers deja charges et leur informations
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


@mayapp.route('/extracting/', methods=['GET', 'POST'])
# @mayapp.route('/extracting/<filename>/', methods=['GET', 'POST'])
@login_required
def display_extracting_progress():
    """
        Cette vue affiche la page languages.html, c'est une page qui affiche les fichiers deja charges et leur informations
    """

    doc_uploaded = upload_controler.display_uploaded_docs()

    # docu_upl, tabl_cover = ocr_extraction.show_cover_pages_name()

    document = ocr_extraction.show_cover_pages_name()

    if document is None:

        print('RIENNN')

    # ocr_extraction.show_each_file_images(filename)

    # return render_template('doc_scanner_pages/extracting.html', cover_pages=document, docss=doc_uploaded)
    return render_template('doc_scanner_pages/extracting.html', cover_pages=document, docss=doc_uploaded)


@mayapp.route('/extracting/<filename>/', methods=['GET', 'POST'])
@login_required
def display_file_images_progression(filename):

    doc_uploaded = upload_controler.display_uploaded_docs()

    # docu_upl, tabl_cover = ocr_extraction.show_cover_pages_name()

    document = ocr_extraction.show_cover_pages_name()

    # f_images = ocr_extraction.show_each_file_images(filename)
    f_images = ocr_extraction.show_each_file_pages_images(filename)

    return render_template('doc_scanner_pages/extracting.html', cover_pages=document, files_images=f_images)


@mayapp.route('/extracted/', methods=['GET', 'POST'])
@login_required
# def display_file_and_extracted_pages():
def display_extracted_pages_name():

    extracted_files = ExtractedFilesForm()

    # files_list = [(i.id_doc, i.name_doc) for i in applicationModel.DocumentAdded.query.all()]

    docs_name = applicationModel.DocumentAdded.query.all()

    # extracted_files.files_name.choices = files_list
    # extracted_files.files_pages.choices = files_list

    # if extracted_files.files_name.

    return render_template('doc_scanner_pages/extracted.html', form=extracted_files, docs=docs_name)


@mayapp.route('/extracted/<filename>/', methods=['GET', 'POST'])
@login_required
def display_spec_extr_page_nums(filename):

    extracted_files = ExtractedFilesForm()

    name_pdf_extension = filename + '.pdf'

    file_pages = applicationModel.DocumentAdded.query.filter_by(name_doc=name_pdf_extension).first()

    docs_name = applicationModel.DocumentAdded.query.all()

    # files_list = [(i.id_doc, i.name_doc) for i in applicationModel.DocumentAdded.query.all()]

    # extracted_files.files_name.choices = files_list
    # extracted_files.files_pages.choices = files_list

    # if extracted_files.files_name.

    return render_template('doc_scanner_pages/extracted.html', form=extracted_files, strt_page=file_pages.scan_start_doc, end_page=file_pages.scan_end_doc, docs=docs_name, name_of_file=filename)


@mayapp.route('/extracted/<filename>/<numpage>/', methods=['GET', 'POST'])
@login_required
def display_file_and_extracted_pages(filename, numpage):
    extracted_files = ExtractedFilesForm()

    name_pdf_extension = filename + '.pdf'

    file_pages = applicationModel.DocumentAdded.query.filter_by(name_doc=name_pdf_extension).first()

    # files_list = [(i.id_doc, i.name_doc) for i in applicationModel.DocumentAdded.query.all()]
    #
    # extracted_files.files_name.choices = files_list
    # extracted_files.files_pages.choices = files_list

    docs_name = applicationModel.DocumentAdded.query.all()

    page_image = '/app_ressources/translator_ressources/converted_files/' + filename + '/' + filename + '__page_' + numpage + '.jpg'
    page_text_path = 'az_app/app_ressources/translator_ressources/txt_extracted_files/' + filename + '/' + filename + '__page_' + numpage + '.txt'
    page_text = open(page_text_path, 'r').read()


    # print(page_text)


    # if extracted_files.files_name.

    if request.method == 'POST':
        print('POPPPPPPPPPPP')
        page_text_opened = open(page_text_path, 'w+')
        page_text_opened.write(request.form['text_to_correct'])
        print('CHANGES ARE MADE!!!!!!!!')


    return render_template('doc_scanner_pages/extracted.html', form=extracted_files, strt_page=file_pages.scan_start_doc, end_page=file_pages.scan_end_doc, page_image=page_image, page_text=page_text, docs=docs_name, name_of_file=filename)


# FIN DES VUES POUR LE SCAN DES FICHIERS


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


# DEBUT DES VUES POUR LA CREATTION DES UTILISATEURS DE L'APPLICATION ELLE-MEME(NON PAS LE SITE DE TRADUCTION)


@mayapp.route('/users/', methods=['GET', 'POST'])
@login_required
def show_users():
    """
        Cette vue affiche la page languages.html, c'est une page simple qui affiche un popup des langues de traduction utilisées
    """

    all_users = account_controler.display_server_users()

    for us in all_users:

        print(us.fname_admin)

    # print(all_users)

    return render_template('admin_user_pages/users_list.html', users=all_users)

# FIN DES VUES POUR LA CREATTION DES UTILISATEURS DE L'APPLICATION ELLE-MEME(NON PAS LE SITE DE TRADUCTION)


@mayapp.route('/surfers/', methods=['GET', 'POST'])
@login_required
def show_surfers():
    """
        Cette vue affiche la page languages.html, c'est une page simple qui affiche un popup des langues de traduction utilisées
    """

    return render_template('surfer_user_pages/surfer_list.html')

# FIN DES VUES POUR LA CREATTION DES UTILISATEURS DE L'APPLICATION ELLE-MEME(NON PAS LE SITE DE TRADUCTION)






