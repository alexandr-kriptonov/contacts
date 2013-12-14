# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql, uic  # подключает основные модули PyQt
from db import *
from google_thread import GoogleThread
import logging
from classes.mainclass import MainClass
from classes.mainslots import AllSlots


# прототип главной формы
class MainForm(QtGui.QMainWindow, MainClass, AllSlots):

    # конструктор
    def __init__(self):
        super(MainForm, self).__init__()

        # динамически загружает визуальное представление формы
        uic.loadUi("ui/mainform.ui", self)

        dbase = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        #файл базы
        dbase.setDatabaseName('database.db')
        dbase.open()

        # view = self.tV_contacts()
        model = QtSql.QSqlTableModel()
        model.setTable('contacts')
        model.select()
        model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.tV_contacts.setModel(model)

        self.logger = logging.getLogger(__name__)
        self.logger.debug("START!")

        self.google_thread = GoogleThread()
        self.add_to_db_thread = Add_to_DBThread()
        self.get_contacts_into_db_thread = Get_Contacts_into_DB()
        # self.get_contacts_into_db_thread.start()

        self.connect_all_slots()
