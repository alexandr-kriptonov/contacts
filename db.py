# -*- coding: utf-8 -*-
import sqlalchemy as sa
from sqlalchemy.orm import mapper, sessionmaker
from PyQt4.QtCore import *

engine = sa.create_engine("sqlite:///database.db", echo=True)
metadata = sa.MetaData()

contacts_table = sa.Table("contacts", metadata,
                        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
                        sa.Column("id_google", sa.String),
                        sa.Column("full_name", sa.String),
                        sa.Column("birthday", sa.String),
                        sa.Column("email", sa.String),
                        sa.Column("phone", sa.String),
                       )
metadata.create_all(engine)

class Contact(object):

    def __init__(self, id_google, full_name, birthday, email, phone):
        self.id_google = id_google
        self.full_name = full_name
        self.birthday = birthday or ""
        self.email = email or ""
        self.phone = phone or ""

    def __repr__(self):
        return 'Contact: %s' % dict([
            (k,v) for k,v in self.__dict__.items() if not k.startswith('_')])

mapper(Contact, contacts_table)
Session = sessionmaker(bind = engine)

class Add_to_DBThread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.db_contacts = {}
    def run(self):
        self.emit(SIGNAL("db_signal(QString)"), "OPEN SESSION TO DB!")
        self.msleep(100)
        self.emit(SIGNAL("set_db_status"), True)
        self.session = Session()
        self.emit(SIGNAL("set_progress_bar"), 0)
        self.sleep(1)
        try:
            count = 0
            for i in self.db_contacts:
                count += 1

            round_percent = int(round(100/count))

            for i in self.db_contacts:
                self.emit(SIGNAL("db_signal(QString)"), "contact(%s) processed" % self.db_contacts[i]["full_name"])
                contact_to_db = Contact(
                    self.db_contacts[i]["id_google"],
                    self.db_contacts[i]["full_name"],
                    self.db_contacts[i]["birthday"],
                    self.db_contacts[i]["email"],
                    self.db_contacts[i]["phone"]
                    )
                c = self.session.query(Contact).filter_by(id_google=self.db_contacts[i]["id_google"]).first()
                if not c:
                    self.session.add(contact_to_db)
                    self.log.info(u"add contact(%s)!" % self.db_contacts[i]["full_name"])
                else:
                    self.log.info(u"contact(%s) exists!" % self.db_contacts[i]["full_name"])
                self.session.commit()
                self.emit(SIGNAL("set_progress_bar"), i*round_percent)
                self.msleep(1)
        except Exception, e:
            self.log.error(u"%s" % e.message)
        self.emit(SIGNAL("set_progress_bar"), 100)
        self.emit(SIGNAL("db_signal(QString)"), "Disconnected from DB")
        self.emit(SIGNAL("set_db_status"), False)

class Get_Contacts_into_DB(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.db_contacts = {}
    def run(self):
        self.emit(SIGNAL("db_signal(QString)"), "OPEN SESSION TO DB!")
        self.msleep(100)
        self.emit(SIGNAL("set_db_status"), True)
        self.session = Session()
        self.emit(SIGNAL("set_progress_bar"), 0)
        self.sleep(1)

        try:
            for contact in self.session.query(Contact):
                print contact, "\n\n"
        except Exception, e:
            self.log.error(u"%s" % e.message)