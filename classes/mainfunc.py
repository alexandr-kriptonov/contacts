# -*- coding: utf-8 -*-
import classes.dbconnection as dbconnection
from PyQt4 import QtSql


class MainFunc(object):

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

    def lV_main_on_click(self):
        current_name = unicode(self.lV_main.currentIndex().data().toString())
        if self.create_edit_contact_model(current_name):
            self.set_edit_contact_data()
            self.b_edit_contact.setDisabled(False)

    def b_edit_contact_on_click(self):
        self.all_data_contact_setDisabled(False)
        self.b_edit_contact.setDisabled(True)

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

    def create_edit_contact_model(self, contact_name=u""):
        try:
            self.edit_contact_model = QtSql.QSqlTableModel(self)
            self.edit_contact_query = \
                """
                SELECT * from contacts
                WHERE full_name LIKE '%s';
                """ \
            % contact_name
            self.edit_contact_model.setQuery(
                QtSql.QSqlQuery(self.edit_contact_query))
            self.to_log(
                "INFO",
                """
                %s"""
                % self.edit_contact_query)
            return True
        except Exception, e:
            self.to_log(
                "EXCEPT",
                """
                %s"""
                % e.message)
            return False

    def set_edit_contact_data(self):
        try:
            self.le_full_name.setText(
                self.edit_contact_model.record(0).value(u"full_name").toString())

            self.le_phone.setText(
                self.edit_contact_model.record(0).value(u"phone").toString())

            self.le_birthday.setText(
                self.edit_contact_model.record(0).value(u"birthday").toString())

            self.le_email.setText(
                self.edit_contact_model.record(0).value(u"email").toString())

            self.le_id_google.setText(
                self.edit_contact_model.record(0).value(u"id_google").toString())
        except Exception, e:
            self.to_log(
                "EXCEPT",
                """
                %s"""
                % e.message)
            return False

    def all_data_contact_setDisabled(self, value):
        self.le_full_name.setDisabled(value)
        self.le_phone.setDisabled(value)
        self.le_birthday.setDisabled(value)
        self.le_email.setDisabled(value)
        self.le_id_google.setDisabled(value)
        self.b_submit.setDisabled(value)
        self.b_revert.setDisabled(value)

    def b_submit_on_click(self):
        print dir(self.edit_contact_model.record(0).value(u"full_name"))
        # self.edit_contact_model.record(0).value(u"full_name") = \
        #     unicode(self.le_full_name.text)
        # self.edit_contact_model.record(0).value(u"phone") = \
        #     unicode(self.le_phone.text)
        # self.edit_contact_model.record(0).value(u"birthday") = \
        #     unicode(self.le_birthday.text)
        # self.edit_contact_model.record(0).value(u"email") = \
        #     unicode(self.le_email.text)
        # self.edit_contact_model.record(0).value(u"id_google") = \
        #     unicode(self.le_id_google.text)
        self.edit_contact_model.database().transaction()
        if self.edit_contact_model.submitAll():
            self.edit_contact_model.database().commit()
        else:
            self.edit_contact_model.database().rollback()
            QtGui.QMessageBox.warning(
                self,
                "Editor DB",
                "The database reported an error: %s"
                % self.edit_contact_model.lastError().text()
            )
        self.all_data_contact_setDisabled(True)
