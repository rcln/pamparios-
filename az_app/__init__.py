from .models import adminUserModel, applicationModel

from .views.admin_views_route import mayapp

adminUserModel.db_con.init_app(mayapp)
applicationModel.db_con.init_app(mayapp)