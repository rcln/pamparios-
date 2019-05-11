
from ..models import applicationModel
from datetime import datetime
import os


def upload_document(name_doc, owner_doc, lang_doc, scan_start_doc, scan_end_doc, numb_pages_doc, file_saved_in_blob):

    '''
        This function is designed to save uploaded document information and data to the database
    '''

    language_owner = applicationModel.LanguagesApp.query.filter_by(id_lang=lang_doc).first()

    doc = applicationModel.DocumentAdded(name_doc=name_doc,
                                         owner_doc=owner_doc,
                                         lang_doc=lang_doc,
                                         scan_start_doc=scan_start_doc,
                                         scan_end_doc=scan_end_doc,
                                         numb_pages_doc=numb_pages_doc,
                                         file_saved_in_blob=file_saved_in_blob,
                                         date_upload_doc=datetime.utcnow(),
                                         ownlang=language_owner)

    applicationModel.db_con.session.add(doc)
    applicationModel.db_con.session.commit()
    return True


def display_uploaded_docs():
    '''
        This function is designed to display uploaded document's information in the database
    '''

    upl_docs = applicationModel.DocumentAdded.query.all()

    return upl_docs


def browse_cover_pages():

    for root, dirs, files in os.walk("az_app/translator_ressources/files_first_page_image/"):
        for filename in files:
            print(filename)
