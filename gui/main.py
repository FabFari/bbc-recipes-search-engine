import sys
import webbrowser
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QUrl
from gui.main_view import Ui_MainWindow
from gui.web_view import Ui_WebContent
from search_engine.query_engine import perform_query
from search_engine.query_engine import setup_query_engine

class QCustomQWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtGui.QVBoxLayout()
        self.textUpQLabel = QtGui.QLabel()
        self.textDownQLabel = QtGui.QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QtGui.QHBoxLayout()
        self.iconQLabel = QtGui.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet(''' color: rgb(0, 0, 255); ''')
        self.textDownQLabel.setStyleSheet('''color: rgb(255, 0, 0); ''')

    def text(self):
        print 'fewe'

    def setNameFile(self, text):
        self.name_file = text

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)

    def setIcon(self, imagePath):
        self.iconQLabel.setPixmap(QtGui.QPixmap(imagePath))

    def getTextUp(self):
        return 'getTextUp'

    def getTextDown(self):
        return 'getTextDown'

    def getIcon(self):
        return 'getIcon'

    def getNameFile(self):
        return self.name_file


class WebContent(QtGui.QMainWindow, Ui_WebContent):
    def __init__(self,parent=None):
        super(Ui_WebContent, self).__init__(parent)
        QtGui.QMainWindow.__init__(self)
        Ui_WebContent.__init__(self)
        self.setupUi(self)

    def setUrl(self,url):
        #web.load(QUrl("http://google.pl"))
        self.webView.load(QUrl(url))


class Window(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.go_button.clicked.connect(self.perform_query)
        self.go_button.setEnabled(False)
        self.query_text.setPlainText("plase wait few seconds, setup_query_engine")
        setup_query_engine()
        self.go_button.setEnabled(True)
        self.query_text.setPlainText("type the query..")

    def perform_query(self):
        query = self.query_text.toPlainText()
        self.go_button.setEnabled(False)
        print 'perform_query "' + str(query) + '" and then enable it'
        if str(query) in 'type the query':
            print 'type the query in the query'

        result = perform_query(str(query))

        listWidget = self.listWidget
        listWidget.clear()
        for r in result:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()

            myQCustomQWidget.setTextUp(r)
            myQCustomQWidget.setTextDown(r)
            myQCustomQWidget.setIcon(r)
            myQCustomQWidget.setNameFile(r)

            # Create QListWidgetItem
            myQListWidgetItem = QtGui.QListWidgetItem(listWidget)

            # add data to retrive when we click the single item
            myQListWidgetItem.setData(QtCore.Qt.UserRole, myQCustomQWidget)

            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())

            # Add QListWidgetItem into QListWidget
            listWidget.addItem(myQListWidgetItem)
            listWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)

        # self.setCentralWidget(listWidget)
        listWidget.itemClicked.connect(self.item_click)
        listWidget.show()
        self.go_button.setEnabled(True)

    def item_click(self, item):
        print "You clicked: " + str(item.data(QtCore.Qt.UserRole).toPyObject().getNameFile())
        # now we have to lauch the new window
        url = 'http://www.bbc.co.uk/food/recipes/'+str(item.data(QtCore.Qt.UserRole).toPyObject().getNameFile())
        #url = 'http://www.bbc.co.uk/food/recipes/cappucino_crme_brles_08725'
        webbrowser.open(url)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
