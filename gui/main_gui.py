import sys
import webbrowser
from PyQt4 import QtCore, QtGui
from gui.main_view import Ui_MainWindow
from search_engine.query_engine import perform_query
from search_engine.query_engine import setup_query_engine
import urllib2
from multiprocessing.pool import ThreadPool

RECIPES_DIR = "recipes"


# class of custom line when the resuls of the search have to show to the user
class QCustomQWidget(QtGui.QWidget):
    """A single element of the listWidget (list of the results

        Summary:
            This class is used to maintain the information of a single
            element of the listWidget. It's used to construct the single entry of
            the list where there are four major informations


        Attributes:
            filename = file name of the web page to see
            textUpQLabel = the recipe's title
            textDownQLabel = one description's part
            iconQLabel = the image associate to that recipe
    """
    def __init__(self, parent=None):
        """QCustomQWidget's __init__ method

                    ParsedEntry's __init__ method.

                    :param parent: gui object
                    :return: Nothing (void)
        """
        super(QCustomQWidget, self).__init__(parent)
        self.filename = None
        self.pixmap = None
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

    def get_filename(self):
        """To retrieve the QCustomQWidget's filename value
                :return: The QCustomQWidget's filename value
        """
        return self.filename

    def set_filename(self, text):
        """To updated the QCustomQWidget's filename value

               :param text: The new QCustomQWidget's filename value
               :return: Nothing (void)
        """
        self.filename = text

    def set_text_up(self, text):
        """To updated the QCustomQWidget's textUpQLabel value

               :param text: The new QCustomQWidget's textUpQLabel value
               :return: Nothing (void)
        """
        self.textUpQLabel.setText(text)

    def set_text_down(self, text):
        """To updated the QCustomQWidget's textDownQLabel value

               :param text: The new QCustomQWidget's textDownQLabel value
               :return: Nothing (void)
        """
        self.textDownQLabel.setText(text)

    # set the image, from the url we have to download
    def set_icon(self, image_path):
        """To updated the QCustomQWidget's iconQLabel value

               It downloads the image from bbc website, resize and set
               :param image_path: image's url
               :return: Nothing (void)
        """
        data = urllib2.urlopen(image_path).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        width = 40
        height = 40
        self.iconQLabel.setMinimumSize(width, height)
        self.iconQLabel.setMaximumSize(width, height)
        self.iconQLabel.resize(width, height)
        self.pixmap = QtGui.QPixmap(image)
        self.pixmap = self.pixmap.scaledToWidth(74)
        self.iconQLabel.setPixmap(self.pixmap)


    def item_click(self, item):
        """When one item og the listWidget is clicked it launch the browser

               It retrive the QCustomQWidget and the filename attribute. From the last one information
               it can build a url that aims to the bbc web page
               :param item: listWidget item
               :return: Nothing (void)
        """
        print "[main_gui] You clicked: " + str(item.data(QtCore.Qt.UserRole).toPyObject().get_filename())
        # now we have to lauch the new window
        # print str(item.data(QtCore.Qt.UserRole).toPyObject().get_filename())
        url = 'http://www.bbc.co.uk/food/recipes/' + str(item.data(QtCore.Qt.UserRole).toPyObject().get_filename())
        webbrowser.open(url)


class Window(QtGui.QMainWindow, Ui_MainWindow):
    """A single element of the listWidget (list of the results

            Summary:
                This class is used to maintain the information of a single
                element of the listWidget. It's used to construct the single entry of
                the list where there are four major informations


            Attributes:
                go_button = button
                query_text = space where the query is typed
                listWidget = where the results are shown
            """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # when the go button is clicked we perform the query
        self.go_button.clicked.connect(self.perform_query)
        self.go_button.setEnabled(False)
        print "plase wait few seconds, setup_query_engine"
        self.query_text.setPlainText("plase wait few seconds, setup_query_engine")
        setup_query_engine()
        self.go_button.setEnabled(True)
        self.query_text.setPlainText("type the query..")

    def perform_query(self):
        """When one go button is clicked this function is called

              In this method we launch the thread for gui purpose
              :param item: Nothing (void)
              :return: Nothing (void)
        """
        list_widget = self.listWidget
        list_widget.clear()
        list_widget.show()

        self.go_button.setEnabled(False)
        query = self.query_text.toPlainText()
        # launch the thread for gui purpose
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(self.worker, (query, self.checkBox.isChecked()))  # tuple of args for foo
        result = async_result.get()

        # build eache line of QCustomQWidget
        if len(result) != 0:
            for r in result:
                if r == "No result found":
                    my_q_custom_q_widget = QCustomQWidget()

                    my_q_custom_q_widget.set_filename("")
                    my_q_custom_q_widget.set_text_up("No result found")
                    my_q_custom_q_widget.set_text_down("No result found")
                else:
                    # Create QCustomQWidget
                    my_q_custom_q_widget = QCustomQWidget()

                    my_q_custom_q_widget.set_filename(str(r.get_name()))

                    if r.get_title() is not None:
                        my_q_custom_q_widget.set_text_up(r.get_title())
                    if r.get_desc() is not None:
                        my_q_custom_q_widget.set_text_down(r.get_desc())
                    if r.get_img_url() is not None:
                        my_q_custom_q_widget.set_icon(str(r.get_img_url()))

                # Create QListWidgetItem
                my_qlist_widget_item = QtGui.QListWidgetItem(list_widget)

                # add data to retrive when we click the single item
                my_qlist_widget_item.setData(QtCore.Qt.UserRole, my_q_custom_q_widget)

                # Set size hint
                my_qlist_widget_item.setSizeHint(my_q_custom_q_widget.sizeHint())

                # Add QListWidgetItem into QListWidget
                list_widget.addItem(my_qlist_widget_item)
                list_widget.setItemWidget(my_qlist_widget_item, my_q_custom_q_widget)

            # self.setCentralWidget(list_widget)
            list_widget.itemClicked.connect(my_q_custom_q_widget.item_click)
            list_widget.show()

        self.go_button.setEnabled(True)
        return

    def worker(self, query, check):
        """Thread's payload

              In this method we launch the thread for gui purpose
              :param query: text query to perform
              :param check: vegetarian checkbox's status
              :return: result: the firs top ten query result
        """
        print '[main_gui] perform_query "' + str(query) + '"'
        result = []
        if str(query) in 'type the query..' or str(query) in "":
            print '[main_gui] type the query'
        else:
            # thread payload
            result = perform_query(str(query), check)
            if len(result) == 0:
                result.append('No result found')
        return result


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
