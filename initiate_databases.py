
from az_app.views.admin_views_route import mayapp
from az_app.models import adminUserModel, surferUserModel, applicationModel


@mayapp.cli.command()
def initiatedbashhhh():
    adminUserModel.init_db()
    surferUserModel.init_db()
    applicationModel.init_db()
