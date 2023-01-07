"""Контекстное меню параметров для выполнения заданных действий
Программисты Прудничленков Г.В., Головка Р.А., Сосальцев В.Р."""

import sys
import sqlite3

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt, QEvent, QObject, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QStandardItemModel, QStandardItem, QKeySequence, QInputEvent, QMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QToolBar, QToolTip, QMessageBox, QWidget, \
    QLabel, QLineEdit, QTreeView, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QScrollBar, QGridLayout, QShortcut, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Конструктор контекстных меню')
        screen = app.primaryScreen()
        size = screen.size()
        self.resize(size.width(), size.height())

        self.setMouseTracking(True)

        self.createMenuBar()

    def createMenuBar(self):

        menuBar = self.menuBar()
        fileMenu = QMenu("File", self)
        editMenu = menuBar.addMenu("Edit")
        helpMenu = menuBar.addMenu("Help")
        menuBar.addMenu(fileMenu)
        menuBar.addMenu(editMenu)
        menuBar.addMenu(helpMenu)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()