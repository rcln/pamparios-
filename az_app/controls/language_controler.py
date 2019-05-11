
from ..models import applicationModel


def create_new_language(lang, desc):

    '''
        This function is designed to insert new translation's language into the database
    '''

    the_language = applicationModel.LanguagesApp(language=lang, description=desc)

    applicationModel.db_con.session.add(the_language)

    applicationModel.db_con.session.commit()

    return True


def display_available_languages():
    '''
        This function is designed to read the translation's language in the database
    '''

    all_langs = applicationModel.LanguagesApp.query.all()

    return all_langs
