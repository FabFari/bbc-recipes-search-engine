import sys
import webbrowser
from PyQt4 import QtCore, QtGui
from gui.main_view import Ui_MainWindow
from search_engine.query_engine import perform_query
from search_engine.query_engine import setup_query_engine
import urllib2
from multiprocessing.pool import ThreadPool

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

    def set_name_file(self, text):
        self.name_file = text

    def set_text_up(self, text):
        self.textUpQLabel.setText(text)

    def set_text_down(self, text):
        self.textDownQLabel.setText(text)

    def set_icon(self, image_path):
        if len(image_path) > 0:
            data = urllib2.urlopen(image_path).read()
            image = QtGui.QImage()
            image.loadFromData(data)
            width = 40
            height = 40
            self.iconQLabel.setMinimumSize(width, height)
            self.iconQLabel.setMaximumSize(width, height)
            self.iconQLabel.resize(width, height)
            self.pixmap = QtGui.QPixmap(image)
            self.pixmap = pixmap.scaledToWidth(74)
            self.iconQLabel.setPixmap(self.pixmap)

    def get_name_file(self):
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
        self.go_button.setEnabled(False)
        query = self.query_text.toPlainText()
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(self.worker, (query, self.checkBox.isChecked()))  # tuple of args for foo
        result = async_result.get()

        list_widget = self.listWidget
        list_widget.clear()
        for r in result:
            # Create QCustomQWidget
            my_q_custom_q_widget = QCustomQWidget()

            my_q_custom_q_widget.set_name_file(r.get_name())
            my_q_custom_q_widget.set_text_up(r.get_title())
            my_q_custom_q_widget.set_text_down(r.get_desc())
            my_q_custom_q_widget.set_icon(r.get_img_url())

            # Create QListWidgetItem
            myQListWidgetItem = QtGui.QListWidgetItem(list_widget)

            # add data to retrive when we click the single item
            myQListWidgetItem.setData(QtCore.Qt.UserRole, my_q_custom_q_widget)

            # Set size hint
            myQListWidgetItem.setSizeHint(my_q_custom_q_widget.sizeHint())

            # Add QListWidgetItem into QListWidget
            list_widget.addItem(myQListWidgetItem)
            list_widget.setItemWidget(myQListWidgetItem, my_q_custom_q_widget)

        # self.setCentralWidget(list_widget)
        list_widget.itemClicked.connect(self.item_click)
        list_widget.show()

        self.go_button.setEnabled(True)
        return

    @staticmethod
    def worker(self, query, check):
        print '[main_gui] perform_query "' + str(query) + '"'
        if str(query) in 'type the query':
            print '[main_gui] type the query in the query'
        else:
            result = perform_query(str(query),check)

            if len(result) == 0:
                result.append('No result found')
            return result

    @staticmethod
    def item_click(item):
        print "[main_gui] You clicked: " + str(item.data(QtCore.Qt.UserRole).toPyObject().get_name_file())
        # now we have to lauch the new window
        url = 'http://www.bbc.co.uk/food/recipes/'+str(item.data(QtCore.Qt.UserRole).toPyObject().get_name_file())
        webbrowser.open(url)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
