
from ..models import applicationModel


def create_new_language(lang, desc):

    the_language = applicationModel.LanguagesApp(language=lang, description=desc)

    applicationModel.db_con.session.add(the_language)

    applicationModel.db_con.session.commit()

    return True


def display_available_languages():

    all_langs = applicationModel.LanguagesApp.query.all()

    return all_langs
