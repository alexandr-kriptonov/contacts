# -*- coding: utf-8 -*-
from PyQt4.QtCore import SIGNAL
from PyQt4 import QtCore, QtSql
import classes.dbconnection as dbconnection
from ui.editdb import EditDBForm


class AllSlots(object):
    """Action & his action"""
    def __init__(self):
        super(AllSlots, self).__init__()

    def connect_all_slots(self):
        self.connect_main_slots()
        self.connect_google_thread_slots()
        self.connect_add_db_thread_slots()

    def connect_google_thread_slots(self):
        self.connect(
            self.b_get_from_google,
            SIGNAL(
                "clicked()"),
            self.b_get_from_google_on_click)

        self.connect(
            self.google_thread,
            SIGNAL(
                "started()"),
            self.google_thread_on_started)

        self.connect(
            self.google_thread,
            SIGNAL(
                "finished()"),
            self.google_thread_on_finished)

        self.connect(
            self.google_thread,
            SIGNAL(
                "set_status_bar"),
            self.set_StatusBar,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.google_thread,
            SIGNAL(
                "thread_error"),
            self.google_thread_error,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.google_thread,
            SIGNAL(
                "set_my_status"),
            self.set_google_status,
            QtCore.Qt.QueuedConnection)

    def connect_add_db_thread_slots(self):

        self.connect(
            self.add_to_db_thread,
            SIGNAL(
                "set_my_status"),
            self.set_db_status,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.google_thread,
            SIGNAL(
                "set_progress_bar"),
            self.set_progress_bar,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.add_to_db_thread,
            SIGNAL(
                "set_status_bar"),
            self.set_StatusBar,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.add_to_db_thread,
            SIGNAL(
                "set_progress_bar"),
            self.set_progress_bar,
            QtCore.Qt.QueuedConnection)

        self.connect(
            self.add_to_db_thread,
            SIGNAL(
                "finished()"),
            self.add_to_db_thread_on_finished)

    def connect_main_slots(self):
        self.connect(
            self.b_edit_db,
            SIGNAL(
                "clicked()"),
            self.b_edit_db_on_click)

        self.connect(
            self.b_quit,
            SIGNAL(
                "clicked()"),
            self.close)

        self.connect(
            self.le_search,
            SIGNAL(
                "returnPressed()"),
            self.search_query)

        self.search_query()

        self.comboB_search.addItem(u"with the any letter")
        self.comboB_search.addItem(u"with the first letter")
        self.comboB_search.addItem(u"with the last letter")

        self.connect(
            self.comboB_search,
            SIGNAL(
                "currentIndexChanged(QString)"),
            self.comboB_search_currentIndexChanged)

        self.le_search.setText("")

        self.comboB_search_currentIndexChanged()

    def b_get_from_google_on_click(self):
        self.b_get_from_google.setDisabled(True)
        self.google_thread.db_contacts = self.google_thread.start()

    def google_thread_on_started(self):
        # Вызывается при запуске потока
        self.set_StatusBar(u"Вызван метод google_thread_on_started()")

    def google_thread_on_finished(self):
        # Вызывается при завершении потока
        self.b_get_from_google.setDisabled(False)  # Делаем кнопку активной
        # print self.google_thread.db_contacts
        # import pdb; pdb.set_trace()
        if self.google_thread.db_contacts:
            self.add_to_db_thread.db_contacts = self.google_thread.db_contacts
            self.add_to_db_thread.start()

    def google_thread_error(self, TYPE_ERROR, TITLE, MESSAGE):
        self.show_error(TYPE_ERROR, TITLE, MESSAGE)

    def set_db_status(self, value=False):
        if value:
            self.l_db_status.setText("<font color = green>CONNECTED!<\\font>")
        else:
            self.l_db_status.setText("<font color = red>DISCONNECTED!<\\font>")

    def set_google_status(self, value=False):
        if value:
            self.l_google_status.setText("\
                <font color = green>CONNECTED!<\\font>")
        else:
            self.l_google_status.setText("\
                <font color = red>DISCONNECTED!<\\font>")

    def set_progress_bar(self, value):
        value = int(value)
        if(0 <= value <= 100):
            self.pBar.setValue(value)
        elif(value > 100):
            while(value > 100):
                value = value - 100
            self.pBar.setValue(value)

    def set_StatusBar(self, MESSAGE="None"):
        self.statusBar().showMessage(MESSAGE)

    def b_edit_db_on_click(self):
        self.editor = EditDBForm(
            "QSQLITE",
            "database.db",
            "contacts",
            self)
        self.editor.show()
        self.setDisabled(True)

    def add_to_db_thread_on_finished(self):
        self.search_query()

    def search_query(self):
        self.dbdriver = "QSQLITE"
        self.dbname = "database.db"
        self.dbtable = "contacts"

        if dbconnection.createConnection(self.dbdriver, self.dbname):
            self.comboB_search_currentIndexChanged()
            self.model = QtSql.QSqlTableModel(self)
            self.model.setQuery(QtSql.QSqlQuery(self.query_search))
            self.to_log(
                "INFO",
                """
                %s"""
                % self.query_search)
            self.lV_main.setModel(self.model)

    def comboB_search_currentIndexChanged(self):
        _index_search = self.comboB_search.currentIndex()

        if _index_search == 0:
            self.query_search = """
                SELECT full_name from contacts
                WHERE full_name LIKE %s
                ORDER BY full_name;
                """ % (" '%%%s%%' " % self.le_search.text())
            self.l_search.setText("Description: %%text%%")
            return True
        elif _index_search == 1:
            self.query_search = """
                SELECT full_name from contacts
                WHERE full_name LIKE %s
                ORDER BY full_name;
                """ % (" '%s%%' " % self.le_search.text())
            self.l_search.setText("Description: text%%")
            return True
        elif _index_search == 2:
            self.query_search = """
                SELECT full_name from contacts
                WHERE full_name LIKE %s
                ORDER BY full_name;
                """ % (" '%%%s' " % self.le_search.text())
            self.l_search.setText("Description: %%text")
            return True
        else:
            self.query_search = """
                SELECT full_name from contacts
                WHERE full_name LIKE %s
                ORDER BY full_name;
                """ % (" '%%%s%%' " % self.le_search.text())
            self.l_search.setText("Description: %%text%%")
            return True
