# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, QtSql, uic  # подключает основные модули PyQt
from db import *
from google import *
import logging
 
# прототип главной формы
class MainForm(QtGui.QDialog):
 
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

        self.google_thread = GoogleThread()
        self.add_to_db_thread = Add_to_DBThread()
        self.get_contacts_into_db_thread = Get_Contacts_into_DB()
        # self.get_contacts_into_db_thread.start()

        # связывает событие нажатия на кнопку с методом
        self.connect(self.b_get_from_google,
            QtCore.SIGNAL("clicked()"),
            self.b_get_from_google_on_click
            )
        self.connect(self.google_thread,
            QtCore.SIGNAL("started()"),
            self.google_thread_on_started
            )
        self.connect(self.google_thread,
            QtCore.SIGNAL("finished()"),
            self.google_thread_on_finished
            )
        self.connect(self.google_thread,
            QtCore.SIGNAL("google_signal(QString)"),
            self.l_terminal_set_text,
            QtCore.Qt.QueuedConnection
            )
        self.connect(self.add_to_db_thread,
            QtCore.SIGNAL("set_db_status"),
            self.set_db_status,
            QtCore.Qt.QueuedConnection
            )
        self.connect(self.google_thread,
            QtCore.SIGNAL("set_google_status"),
            self.set_google_status,
            QtCore.Qt.QueuedConnection
            )
        self.connect(self.google_thread,
            QtCore.SIGNAL("set_progress_bar"),
            self.set_progress_bar,
            QtCore.Qt.QueuedConnection
            )
        self.connect(self.add_to_db_thread,
            QtCore.SIGNAL("db_signal(QString)"),
            self.l_terminal_set_text,
            QtCore.Qt.QueuedConnection
            )
        self.connect(self.add_to_db_thread,
            QtCore.SIGNAL("set_progress_bar"),
            self.set_progress_bar,
            QtCore.Qt.QueuedConnection
            )
        self.log = logging
        self.log.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'mylog.log')
 
    def b_get_from_google_on_click(self):
        self.b_get_from_google.setDisabled(True)
        self.google_thread.db_contacts = self.google_thread.start()

    def google_thread_on_started(self):
        # Вызывается при запуске потока
        self.l_terminal.setText(u"Вызван метод google_thread_on_started()")

    def google_thread_on_finished(self):
        # Вызывается при завершении потока
        # self.l_terminal.setText(u"Вызван метод google_thread_on_finished()")
        self.b_get_from_google.setDisabled(False) # Делаем кнопку активной
        # print self.google_thread.db_contacts
        self.add_to_db_thread.db_contacts = self.google_thread.db_contacts
        self.add_to_db_thread.log = self.log
        self.add_to_db_thread.start()

    def l_terminal_set_text(self, s):
        self.l_terminal.setText(s)
        # self.file_log.write(unicode(s) + "\n")
        s = unicode(s)
        self.log.info(s)

    def set_db_status(self, value=False):
        if value:
            self.l_db_status.setText("<font color = green>CONNECTED!<\\font>")
        else:
            self.l_db_status.setText("<font color = red>DISCONNECTED!<\\font>")

    def set_google_status(self, value=False):
        if value:
            self.l_google_status.setText("<font color = green>CONNECTED!<\\font>")
        else:
            self.l_google_status.setText("<font color = red>DISCONNECTED!<\\font>")

    def set_progress_bar(self, value):
        value = int(value)
        if(0<=value<=100):
            self.pBar.setValue(value)
        elif(value>100):
            while(value>100):
                value = value - 100
            self.pBar.setValue(value)