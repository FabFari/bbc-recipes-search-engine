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


RECIPES_DIR = "recipes"
recipe = 'hasselback_bacon_61171.html'
result = []
f = io.open('..\{}\{}'.format(RECIPES_DIR, recipe), 'r', encoding='utf-8')
soup = BeautifulSoup(f, 'html5lib')
imgs = check_if_empty(soup.find_all("img", class_="recipe-media__image responsive-images")[0]['src'])
tup = ('jnejw',imgs)

result.append(tup)
tup = ('efwewwefewf',imgs)
result.append(tup)

print result

for r in result:
    print r[0]