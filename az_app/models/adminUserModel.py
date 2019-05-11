
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import *

import logging as lg

from datetime import datetime

import enum

from flask_login import UserMixin

from hashlib import md5


db_con = SQLAlchemy()


class Permission(enum.Enum):

    Ordinary = 0
    Administrator = 1


class AdminsAcount(UserMixin, db_con.Model):

    id_admin = Column(Integer, primary_key=True, autoincrement=True)
    fname_admin = Column(String(200), nullable=False)
    lname_admin = Column(String(200), nullable=False)
    email_admin = Column(String(200), unique=True, nullable=False)
    pass_admin = Column(String(200), nullable=False)
    permission_admin = Column(Enum(Permission), nullable=False)
    date_admin = Column(DateTime, nullable=False, default=datetime.date(datetime.utcnow()))

    def __init__(self, fname_admin, lname_admin, email_admin, pass_admin, permission_admin, date_admin):
        self.fname_admin = fname_admin
        self.lname_admin = lname_admin
        self.email_admin = email_admin
        self.pass_admin = pass_admin
        self.permission_admin = permission_admin
        self.date_admin = date_admin

    def __repr__(self):

        return f"Connexion Admin : Mr '{self.lname_admin}' '{self.fname_admin}', Email : '" \
                            f"{self.email_admin}', Date Inscription : '{self.date_admin}' "

    def get_id(self):

        return self.id_admin


def init_db():
    db_con.drop_all()
    db_con.create_all()
    db_con.session.add(AdminsAcount('Aziz', 'OKOTAN', 'azizokotan@outlook.fr', md5('12345678'.encode()).hexdigest(), 'Administrator', datetime.utcnow()))
    db_con.session.commit()
    lg.warning("Initialisation de la base de donnee...")
