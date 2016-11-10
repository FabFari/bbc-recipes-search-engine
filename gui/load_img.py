import io
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