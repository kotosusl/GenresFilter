import sys
import sqlite3

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        super(Ui_MainWindow, self).__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 348)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(180, 10, 611, 311))
        self.tableView.setObjectName("tableView")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 20, 161, 31))
        self.comboBox.setObjectName("comboBox")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 90, 111, 51))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Фильтрация по жанрам"))
        self.pushButton.setText(_translate("MainWindow", "Пуск"))


class GenreFilter(Ui_MainWindow):
    def __init__(self):
        super(GenreFilter, self).setupUi(self)
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('films_db.sqlite')
        self.project_model = QSqlTableModel(self)
        self.project_model.select()
        sqlquery = QSqlQuery('''SELECT films.title as "Название", films.genre as "Жанр",
                         films.year as "Год" from films''', self.db)
        self.project_model.setQuery(sqlquery)
        self.tableView.setModel(self.project_model)
        self.con = sqlite3.connect("films_db.sqlite")
        self.cur = self.con.cursor()
        self.comboBox.addItems([p[0] for p in self.cur.execute(f'''select genres.title from genres''').fetchall()])
        self.pushButton.clicked.connect(self.get_result)

    def get_result(self):
        print(self.cur.execute(f'''select films.title as "Название", films.genre as "Жанр",
                         films.year as "Год" 
                         from films where films.genre = 
                         (select genres.id 
                         from genres where genres.title = '{self.comboBox.currentText()}')''').fetchall())
        sqlquery = QSqlQuery(f'''select films.title as "Название", films.genre as "Жанр",
                         films.year as "Год" from films where films.genre = 
                         (select genres.id from genres where genres.title = '{self.comboBox.currentText()}')''',
                             self.db)
        self.project_model.setQuery(sqlquery)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = GenreFilter()
    form.show()
    sys.exit(app.exec())
