# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtSql, uic  # подключает основные модули PyQt
import classes.dbconnection as dbconnection


class EditContact(QtGui.QWidget):
    """docstring for EditContact"""
    def __init__(
        self,
        dbdriver,
        dbname,
        dbtable,
        contact_name="",
        MainWindow=None
    ):
        super(EditContact, self).__init__()
        uic.loadUi("ui/editcontact.ui", self)
        self.MainWindow = MainWindow
        self.dbdriver = dbdriver
        self.dbname = dbname
        self.dbtable = dbtable
        self.contact_name = contact_name
        self.MainWindow = MainWindow
        self.set_all()
        self.b_submit.clicked.connect(self.submit)
        self.b_revert.clicked.connect(self.model.revertAll)
        self.b_quit.clicked.connect(self.close)

    def set_all(self):
        self.model = QtSql.QSqlTableModel(self)
        self.query_search = \
            """
            SELECT * from contacts
            WHERE full_name LIKE '%s';
            """ \
        % self.contact_name

        if dbconnection.createConnection(self.dbdriver, self.dbname):

            self.model.setQuery(QtSql.QSqlQuery(self.query_search))
            print "query:", self.query_search
            print "record: %s" % self.model.record(0).value(u"full_name").toString()

            self.le_full_name.setText(
                self.model.record(0).value(u"full_name").toString())
            self.le_phone.setText(
                self.model.record(0).value(u"phone").toString())
            self.le_birthday.setText(
                self.model.record(0).value(u"birthday").toString())
            self.le_email.setText(
                self.model.record(0).value(u"email").toString())
            self.le_id_google.setText(
                self.model.record(0).value(u"id_google").toString())

    def submit(self):
        self.model.database().transaction()
        if self.model.submitAll():
            self.model.database().commit()
        else:
            self.model.database().rollback()
            QtGui.QMessageBox.warning(
                self,
                "Editor contact",
                "The database reported an error: %s"
                % self.model.lastError().text()
            )

    def closeEvent(self, arg):
        self.MainWindow.setDisabled(False)
