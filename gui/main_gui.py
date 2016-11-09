import io
import sys
import webbrowser
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QUrl
from gui.main_view import Ui_MainWindow
from gui.web_view import Ui_WebContent
from search_engine.query_engine import perform_query
from search_engine.query_engine import setup_query_engine
from bs4 import BeautifulSoup
from search_engine.corpus_builder import check_if_empty
from PyQt4.QtGui import *
import urllib2
from PyQt4.QtCore import QUrl
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest


RECIPES_DIR = "recipes"


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
        if(len(imagePath)>0):
            #img =urllib.urlretrieve(imagePath, str(self.name_file)+".jpg")

            # print 'imagePath: '+str(imagePath)
            data = urllib2.urlopen(imagePath).read()
            image = QtGui.QImage()
            image.loadFromData(data)
            width = 40
            height = 40
            self.iconQLabel.setMinimumSize(width, height)
            self.iconQLabel.setMaximumSize(width, height)
            self.iconQLabel.resize(width, height)
            pixmap = QtGui.QPixmap(image)
            pixmap2 = pixmap.scaledToWidth(74)
            #mg.setMinimumSize(width, height)
            #img.setMaximumSize(width, height)
            #img.resize(width,height)
            self.iconQLabel.setPixmap(pixmap2)



    def getTextUp(self):
        return 'getTextUp'

    def getTextDown(self):
        return 'getTextDown'

    def getIcon(self):
        return 'getIcon'

    def getNameFile(self):
        return self.name_file


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
        print '[main_gui] perform_query "' + str(query)+'"'
        if str(query) in 'type the query':
            print '[main_gui] type the query in the query'

        result = perform_query(str(query))
        tag = True
        if len(result) == 0:
            result.append('No result found')
            tag = False

        #print '[main_gui]' + str(result)

        if(tag):
            #recipe, title, descr, img_url
            result = self.getTitleDescIcon(result)

        listWidget = self.listWidget
        listWidget.clear()
        for r in result:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()

            myQCustomQWidget.setNameFile(r[0])
            myQCustomQWidget.setTextUp(r[1])
            myQCustomQWidget.setTextDown(r[2])
            myQCustomQWidget.setIcon(r[3])

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
        print "[main_gui] You clicked: " + str(item.data(QtCore.Qt.UserRole).toPyObject().getNameFile())
        # now we have to lauch the new window
        url = 'http://www.bbc.co.uk/food/recipes/'+str(item.data(QtCore.Qt.UserRole).toPyObject().getNameFile())
        #url = 'http://www.bbc.co.uk/food/recipes/cappucino_crme_brles_08725'
        webbrowser.open(url)

    def getTitleDescIcon(self,res):
        result = []
        for recipe in res:
            recipe = str(recipe) + '.html'
            f = io.open('..\{}\{}'.format(RECIPES_DIR, recipe), 'r', encoding='utf-8')
            soup = BeautifulSoup(f, 'html5lib')

            # print "Name: ",recipe

            title = check_if_empty(soup.find_all("h1", class_='content-title__text'))
            # print "Title:", title

            descr = check_if_empty(soup.find_all("p", class_='recipe-description__text'))
            # print "Description:", descr

            img_url = soup.find_all("img", class_="recipe-media__image responsive-images")
            if(len(img_url)>0):
                img_url = img_url[0]['src']
            else:
                img_url = ''

            #result print 'Image url:', img_url
            tup = (recipe, title, descr, img_url)
            result.append(tup)
            # print '\n'
        # print result
        return result
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
