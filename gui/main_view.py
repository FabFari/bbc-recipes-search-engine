# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_view.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(545, 625)
        MainWindow.setMinimumSize(QtCore.QSize(345, 425))
        MainWindow.setMaximumSize(QtCore.QSize(545, 625))
        font = QtGui.QFont()
        font.setPointSize(13)
        MainWindow.setFont(font)
        MainWindow.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("bbc.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setMaximumSize(QtCore.QSize(800, 559))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.formLayout = QtGui.QFormLayout(self.centralwidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setEnabled(True)
        self.listWidget.setMinimumSize(QtCore.QSize(300, 470))
        self.listWidget.setMaximumSize(QtCore.QSize(500, 490))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.SpanningRole, self.listWidget)
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.checkBox)
        self.go_button = QtGui.QPushButton(self.centralwidget)
        self.go_button.setMinimumSize(QtCore.QSize(45, 35))
        self.go_button.setMaximumSize(QtCore.QSize(45, 28))
        self.go_button.setDefault(False)
        self.go_button.setFlat(False)
        self.go_button.setObjectName(_fromUtf8("go_button"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.go_button)
        self.query_text = QtGui.QPlainTextEdit(self.centralwidget)
        self.query_text.setMinimumSize(QtCore.QSize(200, 35))
        self.query_text.setMaximumSize(QtCore.QSize(450, 35))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.query_text.setFont(font)
        self.query_text.setObjectName(_fromUtf8("query_text"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.query_text)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 545, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionPreproces_Setup = QtGui.QAction(MainWindow)
        self.actionPreproces_Setup.setObjectName(_fromUtf8("actionPreproces_Setup"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Search Engine Recipes", None))
        self.checkBox.setText(_translate("MainWindow", "Vegetarian", None))
        self.go_button.setText(_translate("MainWindow", "GO!", None))
        self.query_text.setPlainText(_translate("MainWindow", "type the query", None))
        self.actionPreproces_Setup.setText(_translate("MainWindow", "Preproces Setup", None))

