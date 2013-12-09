# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, uic, QtSql  # подключает основные модули PyQt

class TableForm(QtGui.QMainWindow):
    # конструктор
    def __init__(self):
        super(TableForm, self).__init__()
        # динамически загружает визуальное представление формы
        uic.loadUi("ui/table.ui", self)

        #подключение база
        dbase = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        #файл базы
        dbase.setDatabaseName('database.db') 
        dbase.open()
        # query=QtSql.QSqlQuery()
        #Создаем базу
        # query.exec_('CREATE TABLE my_table (number integer PRIMARY KEY NOT NULL, address VARCHAR(255), age integer);')
        # query.exec_(u'INSERT INTO my_table(number, address, age) VALUES (1, "Варшавское 2", 54);')
        # query.exec_(u'INSERT INTO my_table(number, address, age) VALUES (2, "Ленина 5", 4);')
        #типа DBGird
        view = self.tableView()
        #типа Table
        model = QtSql.QSqlTableModel()
        model.setTable('contacts')
        model.select()
        model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        view.setModel(model)
        view.show()
