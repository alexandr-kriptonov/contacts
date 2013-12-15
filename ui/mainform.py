# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql, uic  # подключает основные модули PyQt
from db import *
from google_thread import GoogleThread
import logging
from classes.mainclass import MainClass
from classes.mainslots import AllSlots
from classes.mainfunc import MainFunc
import classes.dbconnection as dbconnection


# прототип главной формы
class MainForm(QtGui.QMainWindow, MainClass, AllSlots, MainFunc):

    # конструктор
    def __init__(self):
        super(MainForm, self).__init__()

        # динамически загружает визуальное представление формы
        uic.loadUi("ui/mainform.ui", self)

        self.logger = logging.getLogger(__name__)
        self.set_google_status()
        self.set_db_status()

        self.google_thread = GoogleThread()
        self.add_to_db_thread = Add_to_DBThread()
        self.get_contacts_into_db_thread = Get_Contacts_into_DB()
        # self.get_contacts_into_db_thread.start()

        self.connect_all_slots()

    def closeEvent(self, arg):
        self.to_log("INFO", "CLOSE MAIN WINDOW!")

    def showEvent(self, arg):
        self.to_log("INFO", "SHOW MAIN WINDOW!")
