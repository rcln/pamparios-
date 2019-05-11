
from ..models import adminUserModel
from hashlib import md5
from datetime import datetime


def check_server_login(email, password):

    server_user = adminUserModel.AdminsAcount.query.filter_by(email_admin=email).first()

    if server_user is None:
        return 0
    else:
        if server_user.pass_admin == md5(password.encode()).hexdigest():
            return server_user
        else:
            return 0


def create_server_user(fname, lname, email, permission):

    passwd = md5('12345678'.encode()).hexdigest()

    actual_date = datetime.date(datetime.utcnow())

    server_account = adminUserModel.AdminsAcount(fname, lname, email, passwd, permission, actual_date)

    adminUserModel.db_con.session.add(server_account)

    adminUserModel.db_con.session.commit()

    return True


def display_server_users():

    server_users = adminUserModel.AdminsAcount.query.all()

    return server_users
