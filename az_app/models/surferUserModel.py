
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from ..views.admin_views_route import mayapp
import logging as lg


db_con = SQLAlchemy(mayapp)


class SurfersAcount(db_con.Model):

    id_surfer = Column(Integer, primary_key=True, autoincrement=True)
    nom_surfer = Column(String(200), nullable=False)
    prenom_surfer = Column(String(200), nullable=False)
    email_surfer = Column(String(200), unique=True, nullable=False)
    pass_surfer = Column(String(200), nullable=False)
    date_surfer = Column(Date, nullable=False)

    def __init__(self, nom_surfer, prenom_surfer, email_surfer, pass_surfer, date_surfer):
        self.nom_surfer = nom_surfer
        self.prenom_surfer = prenom_surfer
        self.email_surfer = email_surfer
        self.pass_surfer = pass_surfer
        self.date_surfer = date_surfer

    def __repr__(self):

        return f"Connexion Surfer : Mr '{self.nom_surfer}' '{self.prenom_surfer}', Email : '" \
                            f"{self.email_surfer}', Date Inscription : '{self.date_surfer}' "


def init_db():
    db_con.drop_all()
    db_con.create_all()
    db_con.session.commit()
    lg.warning("Initialisation de la base de donnee...")
