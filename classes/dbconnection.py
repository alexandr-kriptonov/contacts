# -*- coding: utf-8 -*-
from PyQt4 import QtSql, QtGui


def createConnection(dbdriver, dbname):
    db = QtSql.QSqlDatabase.addDatabase(dbdriver)  # "QSQLITE"
    db.setDatabaseName(dbname)  # ":memory:"
    if not db.open():
        QtGui.QMessageBox.critical(
            None,
            QtGui.qApp.tr("Cannot open database"),
            QtGui.qApp.tr(
                "Unable to establish a database connection.\n"
                "This example needs SQLite support. Please read "
                "the Qt SQL driver documentation for information "
                "how to build it.\n\nClick Cancel to exit."),
            QtGui.QMessageBox.Cancel,
            QtGui.QMessageBox.NoButton)
        return False
    return True
