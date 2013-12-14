# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql, uic  # подключает основные модули PyQt
import classes.dbconnection as dbconnection


class EditDBForm(QtGui.QWidget):

    def __init__(self, dbdriver, dbname, dbtable, MainWindow):
        super(EditDBForm, self).__init__()
        uic.loadUi("ui/editdb.ui", self)
        self.dbdriver = dbdriver
        self.dbname = dbname
        self.dbtable = dbtable
        self.MainWindow = MainWindow
        if dbconnection.createConnection(self.dbdriver, self.dbname):
            self.model = QtSql.QSqlTableModel(self)
            self.model.setTable(self.dbtable)
            self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
            self.model.select()
            self.model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
            self.model.setHeaderData(1, QtCore.Qt.Horizontal, "ID Google")
            self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Full name")
            self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Birthday")
            self.model.setHeaderData(4, QtCore.Qt.Horizontal, "email")
            self.model.setHeaderData(5, QtCore.Qt.Horizontal, "Phone")
            self.tableViewMain.setModel(self.model)

            self.b_submit.clicked.connect(self.submit)
            self.b_revert.clicked.connect(self.model.revertAll)
            self.b_quit.clicked.connect(self.close)

    def submit(self):
        self.model.database().transaction()
        if self.model.submitAll():
            self.model.database().commit()
        else:
            self.model.database().rollback()
            QtGui.QMessageBox.warning(
                self,
                "Editor DB",
                "The database reported an error: %s"
                % self.model.lastError().text()
            )

    def closeEvent(self, arg):
        self.MainWindow.setDisabled(False)
