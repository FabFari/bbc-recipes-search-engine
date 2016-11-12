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
    print '----------- get_recipes_by_ingredients called -----------'
    # list of all letter in alphabet
    alpha = list(string.ascii_lowercase)

    links_i_level = [] # links like "http://www.bbc.co.uk/food/ingredients/by/letter/[a-z]"
    #  where [a-z] is like "acidulated_water, onion, ecc"
    links_search = []  # for each first level link we can have a link like:
    # "bbc.co.uk/food/recipes/search?keywords=xxx", we have to save for discover, inside these links, new recipes
    links_recipes = []  # list of all recipes

    print "----------- links_i_level -----------"

    if os.path.isfile(I_LEVEL_INGR_LINKS_FILE):
        # for debug purpose we save a file for each step, so if something go bad (connection error and so on)
        # we can restart without redownload
        print 'file {} exists'.format(I_LEVEL_INGR_LINKS_FILE)
        links_i_level = read_list(I_LEVEL_INGR_LINKS_FILE)
    else:
        print 'file {} not exists'.format(I_LEVEL_INGR_LINKS_FILE)
        # for all letter in alphabet we save all links like "bbc.co.uk/food/acidulated_water" found in, e.g.
        # "bbc.co.uk/food/ingredients/by/letter/a"
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

        # for debug purpose we save in a file
        put_into_file(links_i_level, I_LEVEL_INGR_LINKS_FILE)

    print "----------- linksIIlevel -----------"
    if os.path.isfile(PARTIAL_INGR_LINKS_FILE) and os.path.isfile(SEARCH_TODO_INGR_LINKS_FILE):
        # for debug purpose we save a file for each step, so if something go bad (connection error and so on)
        # we can restart without redownload
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
                    # we shunt two different type of links
                    if 'search' in uri:
                        links_search.append(str(uri).replace(' ', '%20'))
                    elif uri != '/food/recipes/':
                        links_recipes.append(str(uri))
            i += 1
        print '#links_recipes: {}, #links_search: {}'.format(len(links_recipes), len(links_search))

        # for debug purpose we save in a two different files.
        # PARTIAL_INGR_LINKS_FILE because we did not find all recipes
        put_into_file(links_recipes, PARTIAL_INGR_LINKS_FILE)
        put_into_file(links_search, SEARCH_TODO_INGR_LINKS_FILE)

    print "\n----------- links_search -----------"
    # last step
    # for each link in links_search we try to look for a final recipe
    for link in links_search:
        print '[links_search] #links_recipes:', len(set(links_recipes))
        j = 1
        found = True

        print '[links_search]', BASE_URL + str(link).replace(' ', '%20')
        # we have to be careful that one url has different page, so we have to look for also in the others pages
        while found:
            url = BASE_URL + str(link).replace(' ', '%20') + str('&page=') + str(j)
            print '     [links_search] page:', url
            page = open_inf(url)

            # The search goes through all the pages: the counter increases until we finish the pages
            soup = soup_parse(page)
            h3 = soup.find_all("h3", {"class": "error"})

            # check if we finished the pages
            for h in h3:
                if 'No results found' in h.getText():
                    found = False
            if found:
                # if there are results we try to look for a final recipe
                page_links = soup.find_all('a', href=True)
                for l in page_links:
                    uri = l.get('href').encode('utf-8')
                    if '/food/recipes/' in uri and 'search' not in uri:
                        if uri != '/food/recipes/':
                            # add in a list
                            links_recipes.append(l.get('href'))
                j += 1
    # save the final result into the file
    # the file has for each line one link of one recipe, in total 11298 recipes.
    put_into_file(links_recipes, INGR_LINKS_FILE)


def soup_parse(page):
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

# from file name read the content and put each line into the list
def read_list(name):
    in_file = open("..\\{}\\{}".format(INPUT_DIR, name), "r")
    lines = []
    for line in in_file:
        # -1 because in the file there is a new line "\n" and we do not want to save in the list
        lines.append(line[:len(line) - 1])
    print('#size ' + name + ' : ' + str(len(lines)))
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
    from utils.utility_functions import ensure_dir

    ensure_dir(INPUT_DIR)
    ensure_dir(OUTPUT_DIR)
    get_recipes_by_ingredients()
