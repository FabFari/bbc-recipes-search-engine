# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'web_view.ui'
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

class Ui_WebContent(object):
    def setupUi(self, WebContent):
        WebContent.setObjectName(_fromUtf8("WebContent"))
        WebContent.resize(850, 650)
        WebContent.setMinimumSize(QtCore.QSize(850, 650))
        WebContent.setMaximumSize(QtCore.QSize(850, 650))
        font = QtGui.QFont()
        font.setPointSize(13)
        WebContent.setFont(font)
        WebContent.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("bbc.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        WebContent.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(WebContent)
        self.centralwidget.setMaximumSize(QtCore.QSize(800, 559))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.webView = QtWebKit.QWebView(self.centralwidget)
        self.webView.setEnabled(False)
        self.webView.setGeometry(QtCore.QRect(0, 0, 16777215, 16777215))
        self.webView.setMinimumSize(QtCore.QSize(16777215, 16777215))
        self.webView.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        WebContent.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(WebContent)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 850, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        WebContent.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(WebContent)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        WebContent.setStatusBar(self.statusbar)
        self.actionPreproces_Setup = QtGui.QAction(WebContent)
        self.actionPreproces_Setup.setObjectName(_fromUtf8("actionPreproces_Setup"))

        self.retranslateUi(WebContent)
        QtCore.QMetaObject.connectSlotsByName(WebContent)

    def retranslateUi(self, WebContent):
        WebContent.setWindowTitle(_translate("WebContent", "Search Engine Recipes", None))
        self.actionPreproces_Setup.setText(_translate("WebContent", "Preproces Setup", None))

from PyQt4 import QtWebKit

class WebContent(QtGui.QMainWindow, Ui_WebContent):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QMainWindow.__init__(self, parent, f)

        self.setupUi(self)

