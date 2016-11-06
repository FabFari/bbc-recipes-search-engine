'''First you need to download the recipes. We will use the recipes at http://www.bbc.co.uk/food/recipes.
You will need to find a way to download all the recipes from the site. You can use any method
you want. It is important to put some time delay between requests; at least 1sec between two
requests. For that you can use the time.sleep command of Python'''
import urllib2
from bs4 import BeautifulSoup
import string
import os
import socket
import os.path

BASE_URL = "http://www.bbc.co.uk"
BASE_RECIPES_URL = "http://www.bbc.co.uk/food/recipes"
BASE_DISHES_URL = "http://www.bbc.co.uk/food/dishes/by/letter/"
BASE_INGREDIENTS_URL = "http://www.bbc.co.uk/food/ingredients/by/letter/"
COLLECTIONS_PATH = "/food/collections/"

I_LEVEL_INGR_LINKS_FILE = "linksIlevelIngredients.txt"
PARTIAL_INGR_LINKS_FILE = "partiaLinks_pythonIngredients.txt"
SEARCH_TODO_INGR_LINKS_FILE = "linksSearchTodoIngredients.txt"
INGR_LINKS_FILE = "links_pythonIngredients.txt"

INPUT_DIR = "data"
OUTPUT_DIR = "data"


def get_recipes_by_ingredients():
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from utils.utility_functions import open_inf

    print '----------- get_recipes_by_ingredients called -----------'
    alpha = list(string.ascii_lowercase)

    links_i_level = []  # links http://www.bbc.co.uk/food/dishes/by/letter/[a-z]
    links_search = []   # per ogni link di links_i_level posso avere dei link alla ricerca, qua me li salvo
    links_recipes = []  # link ultimi con le ricette

    print "----------- links_i_level -----------"

    if os.path.isfile(I_LEVEL_INGR_LINKS_FILE):
        print 'file {} exists'.format(I_LEVEL_INGR_LINKS_FILE)
        links_i_level = read_list(I_LEVEL_INGR_LINKS_FILE)
    else:
        print 'file {} not exists'.format(I_LEVEL_INGR_LINKS_FILE)
        for letter in alpha:
            url = BASE_INGREDIENTS_URL + letter
            print 'letter: {}, url: {}'.format(letter, url)
            page = open_inf(url)
            soup = BeautifulSoup(page, "html5lib")
            food_elems = soup.findAll("li", {"class": "resource food"})

            for l in food_elems:
                link = l.find('a').get('href')
                links_i_level.append(link)

        print('#linksIlevelIngredients:', len(links_i_level))
        links_i_level.sort()
        put_into_file(links_i_level, I_LEVEL_INGR_LINKS_FILE)

    print "----------- linksIIlevel -----------"
    if os.path.isfile(PARTIAL_INGR_LINKS_FILE) and os.path.isfile(SEARCH_TODO_INGR_LINKS_FILE):
        print 'file links_i_level exists'
        links_recipes = read_list(PARTIAL_INGR_LINKS_FILE)
        links_search = read_list(SEARCH_TODO_INGR_LINKS_FILE)
    else:
        i = 0
        for link in links_i_level:
            print "{} {}".format(i, BASE_URL + link)
            page = open_inf(BASE_URL + link)
            soup = soup_parse(page)
            page_links = soup.find_all('a', href=True)
            for l in page_links:
                uri = l.get('href').encode('utf-8')
                if '/food/recipes/' in uri:
                    if 'search' in uri:
                        links_search.append(str(uri).replace(' ', '%20'))
                    elif uri != '/food/recipes/':
                        links_recipes.append(str(uri))
            i += 1
        print '#links_recipes: {}, #links_search: {}'.format(len(links_recipes), len(links_search))
        put_into_file(links_recipes, PARTIAL_INGR_LINKS_FILE)
        put_into_file(links_search, SEARCH_TODO_INGR_LINKS_FILE)

    print "\n----------- links_search -----------"
    for link in links_search:
        print '[links_search] #links_recipes:', len(set(links_recipes))
        j = 1
        found = True

        print '[links_search]', BASE_URL + str(link).replace(' ', '%20')
        while found:
            url = BASE_URL + str(link).replace(' ', '%20') + str('&page=')+str(j)
            print '     [links_search] page:', url
            page = open_inf(url)

            # The search goes through all the pages: the counter increeases until we finish the pages
            soup = soup_parse(page)
            h3 = soup.find_all("h3", {"class": "error"})

            # check if we finished the pages
            for h in h3:
                if 'No results found' in h.getText():
                    found = False
            if found:
                page_links = soup.find_all('a', href=True)
                for l in page_links:
                    uri = l.get('href').encode('utf-8')
                    if '/food/recipes/' in uri and 'search' not in uri:
                        if uri != '/food/recipes/':
                            links_recipes.append(l.get('href'))
                j += 1

    put_into_file(links_recipes, INGR_LINKS_FILE)


def soup_parse(page):
    i = 1
    while True:
        try:
            soup = BeautifulSoup(page, "html5lib")
            return soup
        except urllib2.URLError as e:
            i += 1
            print "[getSoup]There was an error: %r" % e
        except socket.timeout as e:  # <-------- this block here
            i += 1
            print "[getSoup] Timeout exceeded: %r" % e


def read_list(name):
    in_file = open("..\\{}\\{}".format(INPUT_DIR, name), "r")
    lines = []

    for line in in_file:
        # -1 perche nel file c'e' la new line(\n)
        lines.append(line[:len(line)-1])
    print('#size '+name+' : ' + str(len(lines)))
    lines.sort()

    return lines


def put_into_file(links_recipes, name):
    # remove duplicates
    s = set(links_recipes)

    print '#size {}: {}'.format(name, len(s))

    # save into the file
    out_file = open("..\\{}\\{}".format(OUTPUT_DIR, name), "w")
    for link in s:
        out_file.write(link + '\n')
    out_file.close()


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from utils.utility_functions import ensure_dir
    else:
        from ..utils.utility_functions import ensure_dir

    ensure_dir(INPUT_DIR)
    ensure_dir(OUTPUT_DIR)
    get_recipes_by_ingredients()
