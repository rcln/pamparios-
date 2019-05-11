from .models import adminUserModel, applicationModel

from .views.admin_views_route import mayapp

adminUserModel.db_con.init_app(mayapp)
applicationModel.db_con.init_app(mayapp)
# surferUserModel.db_con.init_app(mayapp)

# IL FAUT OBLIGATOIREMENT EVITER DE METTRE LE UNDERSCORE ( _ ) DANS LE NOM DES METHODES
@mayapp.cli.command()
def initiatedbas():
    adminUserModel.init_db()
    # surferUserModel.init_db()
    applicationModel.init_db()
