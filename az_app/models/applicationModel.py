
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import *

from sqlalchemy.orm import relationship, backref

from .adminUserModel import AdminsAcount

from datetime import datetime

import logging as lg

from sqlalchemy.dialects.mysql import LONGBLOB

db_con = SQLAlchemy()


class LanguagesApp(db_con.Model):

    id_lang = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String(200), unique=True, nullable=False)
    description = Column(String(200), unique=True, nullable=False)
    documents = relationship('DocumentAdded', backref='ownlang')

    def __int__(self, language, description):
        self.language = language
        self.description = description

    def __repr__(self):

        return f"Langue ajoutée : '{self.language}' , description : '{self.description}'"

    def __str__(self):

        return f"{self.language}"


class DocumentAdded(db_con.Model):

    id_doc = Column(Integer, primary_key=True, autoincrement=True)
    name_doc = Column(String(200), unique=True, nullable=False)
    owner_doc = Column(Integer, ForeignKey(AdminsAcount.id_admin, ondelete='CASCADE'), nullable=False)
    lang_doc = Column(Integer, ForeignKey(LanguagesApp.id_lang, ondelete='CASCADE'), nullable=False)
    scan_start_doc = Column(Integer, nullable=False)
    scan_end_doc = Column(Integer, nullable=False)
    numb_pages_doc = Column(Integer, nullable=False)
    file_saved_in_blob = Column(LONGBLOB, nullable=False)
    date_upload_doc = Column(DateTime, default=datetime.date(datetime.utcnow()))

    def __int__(self, name_doc, owner_doc, lang_doc, scan_start_doc, scan_end_doc, numb_pages_doc, file_saved_in_blob, date_upload_doc):

        self.name_doc = name_doc
        self.owner_doc = owner_doc
        self.lang_doc = lang_doc
        self.scan_start_doc = scan_start_doc
        self.scan_end_doc = scan_end_doc
        self.numb_pages_doc = numb_pages_doc
        self.file_saved_in_blob = file_saved_in_blob
        self.date_upload_doc = date_upload_doc

    def __repr__(self):

        return f"Document :{self.name_doc}"


class DocAddedPageProgress(db_con.Model):

    id_pag_progress = Column(Integer, primary_key=True, autoincrement=True)
    id_fk_doc_added = Column(Integer, ForeignKey(DocumentAdded.id_doc, ondelete='CASCADE'), nullable=False)
    doc_added_page_name = Column(String(200), nullable=False, unique=True)
    page_progress = Column(Integer, default=0, nullable=False)
    documents = relationship('DocumentAdded', backref='ownpage')

    def __init__(self, id_fk_doc_added, doc_added_page_name, page_progress):

        self.id_fk_doc_added = id_fk_doc_added
        self.doc_added_page_name = doc_added_page_name
        self.page_progress = page_progress

    def __repr__(self):

        return f"Progression de la page : { self.doc_added_page_name }"


class ExtractedWords(db_con.Model):

    id_extr = Column(Integer, primary_key=True, autoincrement=True)
    id_fk_doc_added = Column(Integer, ForeignKey(DocumentAdded.id_doc, ondelete='CASCADE'), nullable=False)
    word = Column(String(200), unique=True, nullable=False)
    w_height = Column(Integer, nullable=False)
    w_width = Column(Integer, nullable=False)
    w_pos_top = Column(Integer, nullable=False)
    w_pos_left = Column(Integer, nullable=False)

    def __int__(self, id_fk_doc_added, word, w_height, w_width, w_pos_top, w_pos_left, file_saved_in_blob, date_upload_doc):
        self.id_fk_doc_added = id_fk_doc_added
        self.word = word
        self.w_height = w_height
        self.w_width = w_width
        self.w_pos_top = w_pos_top
        self.w_pos_left = w_pos_left


class WordsDictionary(db_con.Model):

    id_wrd_dic = Column(Integer, primary_key=True, autoincrement=True)
    word_spanish = Column(String(200), unique=True, nullable=True)
    word_maya = Column(String(200), unique=True, nullable=True)
    word_adder = Column(Integer, ForeignKey(AdminsAcount.id_admin, ondelete='CASCADE'), nullable=False)

    def __int__(self, word_spanish, word_maya, word_adder):
        self.word_spanish = word_spanish
        self.word_maya = word_maya
        self.word_adder = word_adder


class Alphabets(db_con.Model):

    id_fk_lang = Column(Integer, ForeignKey(LanguagesApp.id_lang, ondelete='CASCADE'), primary_key=True, nullable=False)
    character = Column(String(200), primary_key=True, nullable=True)
    pos_in_alphab = Column(Integer, nullable=False, comment='Position du caracter dans l\'alphabet')

    def __int__(self, id_fk_lang, character, pos_in_alphab):

        self.id_fk_lang = id_fk_lang
        self.character = character
        self.pos_in_alphab = pos_in_alphab


def init_db():

    db_con.drop_all()
    db_con.create_all()
    db_con.session.commit()
    lg.warning("Initialisation de la base de donnee...")
