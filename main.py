import sys, os
import sqlite3

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt, QEvent, QObject, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QStandardItemModel, QStandardItem, QKeySequence, QInputEvent, QMouseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QToolBar, QToolTip, QMessageBox, QWidget, \
    QLabel, QLineEdit, QTreeView, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QScrollBar, QGridLayout, QShortcut, QVBoxLayout, \
    QFileDialog

class paramWindow(QWidget):
    def __init__(self, tree, eventValue, parent, child):
        super(paramWindow, self).__init__()
        self.setWindowTitle('Настройка параметров')
        self.setFixedSize(440, 200)

        self.initUI()

        self.eventValue = eventValue
        self.parent = parent
        self.child = child
        self.tree = tree

    def initUI(self):
        self.button = QPushButton('Show', self)
        self.button.resize(150, 30)
        self.button.move(145, 140)

        self.qle = QLineEdit(self, placeholderText='Enter a keyword to search...', clearButtonEnabled=True)
        self.qle.move(95, 90)

        self.setGeometry(300, 300, 400, 170)
        self.qle.resize(250, 23)

        self.button.clicked.connect(self.btnClose)

        self.qle.setFocus()
        self.show()

        # def name_group(name):
        #     text, i = name.get(), 0
        #     connect = sqlite3.connect('main.db')
        #     cursor = connect.cursor()
        #     cursor.execute("INSERT INTO main(group_name) values(?)", (text,))
        #     connect.commit()
        #     while True:
        #         try:
        #             ('', tk.END, text=text, iid=i, open=False)
        #             break
        #         except:
        #             i += 1
        #             continue

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            text = self.qle.text()
            if len(text) != 0: self.btnClose()

    def btnClose(self):
        if len(self.qle.text()) != 0:
            self.text = self.qle.text()

            self.connect = sqlite3.connect('CMconstruct.db')
            self.cursor = self.connect.cursor()

            if self.eventValue == 1:
                self.cursor.execute("SELECT n FROM CMconstruct WHERE type = ? AND name = ?",
                                    (self.eventValue, self.text,))
                self.child = 0

            if self.eventValue == 2:
                self.cursor.execute("SELECT n FROM CMconstruct WHERE type = ? AND name = ? AND parent = ?",
                                    (self.eventValue, self.text, self.parent,))
            if self.eventValue == 3:
                self.cursor.execute("SELECT n FROM CMconstruct WHERE type = ? AND name = ? AND parent = ? AND child = ?",
                                    (self.eventValue, self.text, self.parent, self.child,))

            data = self.cursor.fetchone()

            if data is None:
                self.item = QTreeWidgetItem(self.tree)
                self.item.setText(0, self.text)

                self.cursor.execute(f"SELECT n FROM CMconstruct")
                data = self.cursor.fetchall()

                self.N = len(data)
                list = (self.N, self.eventValue, self.text, self.parent, self.child)

                self.cursor.executemany("INSERT INTO CMconstruct(n, type, name, parent, child) VALUES(?,?,?,?,?);", (list,))
                self.connect.commit()

                self.close()
            else:
                self.label = QLabel(self)
                self.label.setText("Элемент с таким именем уже существует!")
                self.label.adjustSize()
                self.label.move(60, 40)

                self.show()
            # СДЕЛАТЬ ПРОВЕРКУ ИМЕНИ ПО BD ЧТОБЫ НЕ БЫЛО ОДИНАКОВЫХ ИМЕН
            # if data is None:
            #     ЗАПИСАТЬ ИМЯ В BD
            # else:
            #     self.lbl.setText("Name is not valid")
            #     self.lbl.adjustSize()
class EventFilter(QObject):
    mouseButton_pressed = pyqtSignal()

    def __init__(self, widget):
        super().__init__(widget)
        self._widget = widget
        self.widget.viewport().installEventFilter(self)

    @property
    def widget(self):
        return self._widget

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.MouseButtonPress and source is self.widget.viewport()):
            self.mouseButton_pressed.emit()
        return super(EventFilter, self).eventFilter(source, event)

    # def eventFilter(self, object: QObject, event: QEvent):
    #     if object is self.widget and event.type() == QEvent.MouseButtonPress:
    #         print('OK!')
    #         self.mouseButton_pressed.emit()
    #     return super().eventFilter(object, event)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('\n')
        screen = app.primaryScreen()
        size = screen.size()
        # self.resize(size.width(), size.height())
        self.resize(1280, 720)

        self.setMouseTracking(True)

        self.createMenuBar()
        self.createTables()
        self.DBLoader()
        self.HKsetting()

        self.parent = 0
        self.child = 0

        # eventFilter - вызов класса EventFilter, которому мы передаем наши 3 виджета
        # TreeWidget для обработки событий именно в этих объектах
        eventFilter = EventFilter(self.treeView1)
        eventFilter.mouseButton_pressed.connect(self.handle_tree1)
        eventFilter = EventFilter(self.treeView2)
        eventFilter.mouseButton_pressed.connect(self.handle_tree2)
        eventFilter = EventFilter(self.treeView3)
        eventFilter.mouseButton_pressed.connect(self.handle_tree3)

        self.childEnabled = False
        self.parentEnabled = False
        self.fileIsNew = False
        self.filePath = None
    def mousePressEvent(self, event):
        self.isClicked = False

    #Функции для HK
    def DBhk1(self):

        # self.contextMenu = QMenu(self)
        #
        # self.parent = self.contextMenu.addAction(f"parent   1")
        # self.child = self.contextMenu.addAction(f"child     2")
        # self.param = self.contextMenu.addAction(f"param   3")
        #
        # self.action = self.contextMenu.exec_()

        self.DBinsert(1)
    def DBhk2(self):
        self.DBinsert(2)
    def DBhk3(self):
        self.DBinsert(3)

    #Создание DB
    def DBLoader(self):
        self.connect = sqlite3.connect('CMconstruct.db')
        self.cursor = self.connect.cursor()
        self.cursor.execute("DROP TABLE IF EXISTS CMconstruct")
        self.cursor.execute("""CREATE TABLE CMconstruct(
                    n INTEGER,
                    type INTEGER,
                    name TEXT,
                    parent INTEGER,
                    child INTEGER
                )
                """)
    #Создание HK
    def HKsetting(self):

        # keyboard.add_hotkey("ctrl+a+1", lambda: self.DBinsert(1))
        # keyboard.add_hotkey("ctrl+a+2", lambda: self.DBinsert(2))
        # keyboard.add_hotkey("ctrl+a+3", lambda: self.DBinsert(3))

        # keyboard.wait()

        self.shortcut1 = QShortcut(QKeySequence("Ctrl+q"), self)
        self.shortcut1.activated.connect(self.DBhk1)
        self.shortcut2 = QShortcut(QKeySequence("Ctrl+w"), self)
        self.shortcut2.activated.connect(self.DBhk2)
        self.shortcut3 = QShortcut(QKeySequence("Ctrl+e"), self)
        self.shortcut3.activated.connect(self.DBhk3)
        self.shortcut3 = QShortcut(QKeySequence("Ctrl+x"), self)
        self.shortcut3.activated.connect(self.DBdelete)

    #Обработчики для выполнения eventFilter
    def handle_tree1(self):
        self.isClicked = False
        self.eventValue = 1
    def handle_tree2(self):
        self.isClicked = False
        self.eventValue = 2
    def handle_tree3(self):
        self.isClicked = False
        self.eventValue = 3

    #Функция при нажатии на items
    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def onItemClicked(self, item, column):
        # print(item, column, item.text(column))
        '''НУЖНО ИСПРАВИТЬ И ДОРАБОТАТЬ СЛЕДУЮЩИЕ МОМЕНТЫ:
        1) Сделать привязку элементов к родителю через бд (пока что все элементы создаютя независимо друг от друга)
        2) Доработать все виды сохранения проекта
        3) Настроить работу HK в зависимости от активного элемента
        4) Доделать обновление древ при выборе родителя'''
        self.isClicked = True
        self.name = item.text(column)
        if self.eventValue == 1:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT parent FROM CMconstruct WHERE type = ? AND name = ?", (1, item.text(column),))
            data = self.cursor.fetchall()

            self.parentIndex = data[0][0]

            self.treeView2.clear()
            self.treeView3.clear()

            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT name FROM CMconstruct WHERE type = ? AND parent = ?", (2, self.parentIndex,))
            data = self.cursor.fetchall()
            for i in data:
                self.item = QTreeWidgetItem(self.treeView2)
                self.item.setText(0, str(i[0]))

            self.cursor.execute("SELECT name FROM CMconstruct WHERE type = ? AND parent = ?", (3, self.parentIndex,))
            data = self.cursor.fetchall()
            for i in data:
                self.item = QTreeWidgetItem(self.treeView3)
                self.item.setText(0, str(i[0]))

            self.parentEnabled = True

        if self.eventValue == 2:
            self.childEnabled = True

            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT child FROM CMconstruct WHERE type = ? AND name = ? AND parent = ?", (2, item.text(column), self.parent,))
            data = self.cursor.fetchall()
            try:
                self.childIndex = data[0][0]

                self.treeView3.clear()
                self.cursor.execute("SELECT name FROM CMconstruct WHERE type = ? AND parent = ? AND child = ?", (3, self.parent, self.childIndex))
                data = self.cursor.fetchall()
                for i in data:
                    self.item = QTreeWidgetItem(self.treeView3)
                    self.item.setText(0, str(i[0]))
            except: pass


    #Функция для проверки места вызова contextMenu
    def eventChecker(self, event):

        if (event.x() >= 20 and event.y() >= 30) and (event.x() <= 320 and event.y() <= 440):
            return 1
        elif (event.x() >= 330 and event.y() >= 30) and (event.x() <= 630 and event.y() <= 440):
            return 2
        elif (event.x() >= 640 and event.y() >= 30) and (event.x() <= 940 and event.y() <= 440):
            return 3
        else:
            return 0

    # удаление данных об items из БД
    def DBdelete(self):

        # QTreeWidget.invisibleRootItem(self.treeView1)
        # self.treeView1.currentIndex().row()
        # item = QTreeWidget.invisibleRootItem(self.treeView1).takeChild(self.treeView1.currentIndex().row())
        if self.eventValue == 1: tree = self.treeView1
        if self.eventValue == 2: tree = self.treeView2
        if self.eventValue == 3: tree = self.treeView3

        try:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT * FROM CMconstruct WHERE name = ? AND type = ?", (self.name, self.eventValue,))
            data = self.cursor.fetchone()
            # print('SELECT FOR DELETE: ', data, ' ', self.isClicked)
            if data is not None and self.isClicked:
                # print('data и eventValue при delete = ', data)
                self.cursor.execute("DELETE FROM CMconstruct WHERE name = ? AND type = ?", (self.name, self.eventValue,))
                self.connect.commit()
                self.cursor.close()

                QTreeWidget.invisibleRootItem(tree).takeChild(tree.currentIndex().row())
                # print('Удаленый объект: ', self.name, ' ', self.eventValue)

                self.isClicked = False
            else: pass
        except: pass
    def DBinsert(self, eventValue):

        if eventValue == 1:
            self.parent += 1
            tree = self.treeView1

            self.window = paramWindow(tree, eventValue, self.parent, self.child)
            self.window.show()
        if eventValue == 2:
            if self.parent != 0 and self.parentEnabled:
                self.child += 1
                tree = self.treeView2

                self.window = paramWindow(tree, eventValue, self.parentIndex, self.child)
                self.window.show()
        if eventValue == 3:
            tree = self.treeView3
            if self.parent != 0 and self.child != 0 and self.childEnabled:

                self.window = paramWindow(tree, eventValue, self.parentIndex, self.childIndex)
                self.window.show()

    def saveFile(self):
        pass
    def newFile(self):
        self.fileIsNew = True
        self.close()
    def dropFile(self):
        self.DBLoader()
        self.treeView1.clear()
        self.treeView2.clear()
        self.treeView3.clear()
    def saveAsFile(self):
        fileFilter = 'DBFile (*.db)'
        name = QFileDialog.getSaveFileName(
            parent=self,
            caption='Save File',
            # directory=os.getcwd(),
            filter=fileFilter,
            initialFilter=fileFilter
        )
        try:
            file = open(name[0], 'w')
            file.close()
            self.filePath = name[0]
        except: pass
    def openFile(self):
        fileFilter = 'DBFile (*.db)'
        name = QFileDialog.getOpenFileName(
            parent=self,
            caption='Save File'
            # directory=os.getcwd(),
            # filter=fileFilter,
            # initialFilter=fileFilter
        )
        try:
            file = open(name[0], 'r')
            with file:
                text = file.read()
                print(text)
            file.close()

        except: pass

    # Создание трех рабочих пространств
    def createTables(self):
        '''Просто создал три древа treeview в котором и будут распологаться наши группы подгруппы и параметры'''

        # tree1
        self.treeView1 = QTreeWidget(self)
        self.item1 = QTreeWidgetItem()
        self.treeView1.setHeaderHidden(True)
        self.treeView1.itemClicked.connect(self.onItemClicked)

        self.scroll_bar = QScrollBar(self)
        self.scroll_bar.setStyleSheet("background : white;")
        self.treeView1.setVerticalScrollBar(self.scroll_bar)

        self.treeView1.resize(300, 440)
        self.treeView1.move(160, 120)

        self.treeView1.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView1.customContextMenuRequested.connect(self.context)
        # tree2
        self.treeView2 = QTreeWidget(self)
        self.item2 = QTreeWidgetItem()
        self.treeView2.setHeaderHidden(True)
        self.treeView2.itemClicked.connect(self.onItemClicked)

        self.scroll_bar = QScrollBar(self)
        self.scroll_bar.setStyleSheet("background : white;")
        self.treeView2.setVerticalScrollBar(self.scroll_bar)

        self.treeView2.resize(300, 440)
        self.treeView2.move(470, 120)

        self.treeView2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView2.customContextMenuRequested.connect(self.context)
        # tree3
        self.treeView3 = QTreeWidget(self)
        self.item3 = QTreeWidgetItem()
        self.treeView3.setHeaderHidden(True)
        self.treeView3.itemClicked.connect(self.onItemClicked)

        self.scroll_bar = QScrollBar(self)
        self.scroll_bar.setStyleSheet("background : white;")
        self.treeView3.setVerticalScrollBar(self.scroll_bar)

        self.treeView3.resize(300, 440)
        self.treeView3.move(780, 120)

        self.treeView3.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView3.customContextMenuRequested.connect(self.context)
    # Создание верхнего контекстного меню
    def createMenuBar(self):

        menuBar = self.menuBar()

        fileMenu = QMenu("File", self)
        menuBar.addMenu(fileMenu)

        newAction = QtWidgets.QAction('New', fileMenu)
        newAction.triggered.connect(lambda: self.newFile())
        openAction = QtWidgets.QAction('Open', fileMenu)
        openAction.triggered.connect(lambda: self.openFile())
        saveAction = QtWidgets.QAction('Save', fileMenu)
        saveAction.triggered.connect(lambda: self.saveFile())
        saveAsAction = QtWidgets.QAction('Save as', fileMenu)
        saveAsAction.triggered.connect(lambda: self.saveAsFile())

        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)

        newAction.setShortcut("Ctrl+N")
        openAction.setShortcut("Ctrl+O")
        saveAction.setShortcut("Ctrl+S")
        saveAsAction.setShortcut("Ctrl+Shift+S")

        editMenu = menuBar.addMenu("Edit")
        helpMenu = menuBar.addMenu("Help")

    # контекстное меню по ПКМ
    def context(self, event):
        menu = QtWidgets.QMenu()

        eventlist = [1, 2, 3]

        if self.eventValue == 1: self.tree = self.treeView1
        if self.eventValue == 2: self.tree = self.treeView2
        if self.eventValue == 3: self.tree = self.treeView3

        try:
            self.name = self.tree.itemAt(event).text(0)
            self.isClicked = True
            # print(self.name, self.isClicked)
        except:
            pass

        if self.eventValue in eventlist:
            newAction = QtWidgets.QAction('New', menu)
            newAction.triggered.connect(lambda: self.DBinsert(self.eventValue))

            editAction = QtWidgets.QAction('Edit', menu)

            copyAction = QtWidgets.QAction('Copy', menu)

            pastAction = QtWidgets.QAction('Past', menu)

            deleteAction = QtWidgets.QAction('Delete', menu)
            deleteAction.triggered.connect(lambda: self.DBdelete())

            menu.addAction(newAction)
            menu.addAction(editAction)
            menu.addAction(copyAction)
            menu.addAction(pastAction)
            menu.addAction(deleteAction)

            menu.exec(self.tree.mapToGlobal(event))
    # обработка событий при выходе из приложения
    def closeEvent(self, event):
        # Переопределить closeEvent
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT * FROM CMconstruct")
        data = self.cursor.fetchall()
        if len(data) == 0:
            if self.fileIsNew: pass
            else: event.accept()
        else:
            reply = QtWidgets.QMessageBox.question(
                self, 'Информация',
                "Сохранить изменения перед выходом?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
            if self.fileIsNew:
                if reply == QtWidgets.QMessageBox.Yes:
                    self.saveFile()
                    self.dropFile()
                    event.ignore()
                if reply == QtWidgets.QMessageBox.No:
                    self.dropFile()
                    event.ignore()
                if reply == QtWidgets.QMessageBox.Cancel: event.ignore()
            else:
                if reply == QtWidgets.QMessageBox.Yes:
                    self.saveFile()
                    event.accept()
                if reply == QtWidgets.QMessageBox.No: event.accept()
                if reply == QtWidgets.QMessageBox.Cancel: event.ignore()

        self.fileIsNew = False

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()