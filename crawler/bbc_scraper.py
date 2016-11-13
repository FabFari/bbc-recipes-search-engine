# coding=utf-8
import urllib2
import string
import os
import socket
import os.path

from bs4 import BeautifulSoup
from utils.utility_functions import open_inf

# base url of bbc web site
BASE_URL = "http://www.bbc.co.uk"
# base url of all recipes
BASE_RECIPES_URL = "http://www.bbc.co.uk/food/recipes"
# base url of all recipes divided into different ingredients by letter
BASE_INGREDIENTS_URL = "http://www.bbc.co.uk/food/ingredients/by/letter/"
# we have three different kind of links:
# file txt where are saved all links of different ingredients by letter
I_LEVEL_INGR_LINKS_FILE = "linksIlevelIngredients.txt"
# file txt where are saved not all recipes, partial found whit first level links
PARTIAL_INGR_LINKS_FILE = "partiaLinks_pythonIngredients.txt"
# file txt where are saved all links refer to search link
SEARCH_TODO_INGR_LINKS_FILE = "linksSearchTodoIngredients.txt"
# file txt where are saved all links refer to all recipes
INGR_LINKS_FILE = "links_pythonIngredients.txt"
# directory where are saved files
INPUT_DIR = "data"
OUTPUT_DIR = "data"


def get_recipes_by_ingredients():
    """Download all recipes into bbc web site

            we started from the url http://www.bbc.co.uk/food/ingredients/by/letter/
            scanning in alphabetical order all the ingredients and storing them this is
            called links_i_level and store them in linksLevelIngredients.txt for debug
            purpose.
            Each of these 1° level link in our file pointed to a page which in turn
            contained two different type of links: search and recipe. We built two
            lists, one made of links of the former type, one of links of the latter.
            At this point we started to build our set of links of recipes; links of
            the recipe list of before step were pointing to recipes themselves and
            can be added directly to the set. Conversely links in the search list
            pointed to collections of recipes, we used them to navigate through
            those pages and add the recipe links we had previously missed.

            :param Nothing (void)
            :return: file containing all recipes' link
    """

    print '----------- get_recipes_by_ingredients called -----------'

    alpha = list(string.ascii_lowercase)

    links_i_level = [] # links like "http://www.bbc.co.uk/food/ingredients/by/letter/[a-z]"
    #  where [a-z] is like "acidulated_water, onion, ecc"
    links_search = []  # for each first level link we can have a link like:
    # "bbc.co.uk/food/recipes/search?keywords=xxx", we have to save for discover, inside these links, new recipes
    links_recipes = []  # list of all recipes

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
                # save link in the list
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
        # for each link found in the previous step we try to look for two kind of links:
        # "search" or "recipe", the last one is the final link we tried to find,
        # the first one we have to look for again
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
            url = BASE_URL + str(link).replace(' ', '%20') + str('&page=') + str(j)
            print '     [links_search] page:', url
            page = open_inf(url)

            soup = soup_parse(page)
            h3 = soup.find_all("h3", {"class": "error"})

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
    """ performs BeautifulSoup function in a try-catch paradigm
            :param page: to pass to BeautifulSoup
            :return: parsed document
    """

    i = 1
    while True:
        # since sometimes there is network error, we manage this issue to try indefinitely the function
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
    """ from file name we have to read the content and put each line into the list

            Since e have a files contenting the link downloaded before for debug purpose
            we can read the content without redownload
            :param name : file to read
            :return: list where each element of the list is one line of the file
    """
    in_file = open("..\\{}\\{}".format(INPUT_DIR, name), "r")
    lines = []
    for line in in_file:
        # -1 because in the file there is a new line "\n" and we do not want to save in the list
        lines.append(line[:len(line) - 1])
    print('#size ' + name + ' : ' + str(len(lines)))
    lines.sort()

    return lines


def put_into_file(links_recipes, name):
    """ put into the neme file the content of the list


               :param name: file where to put the content
               :param links_recipes:  list of link
               :return: Nothing(void)
    """
    # remove duplicates
    s = set(links_recipes)

    print '#size {}: {}'.format(name, len(s))

    # save into the file
    out_file = open("..\\{}\\{}".format(OUTPUT_DIR, name), "w")
    for link in s:
        out_file.write(link + '\n')
    out_file.close()

if __name__ == '__main__':
    from utils.utility_functions import ensure_dir

    ensure_dir(INPUT_DIR)
    ensure_dir(OUTPUT_DIR)
    get_recipes_by_ingredients()
