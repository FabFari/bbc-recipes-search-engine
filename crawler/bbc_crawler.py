import urllib2
import re
import time
import string

#####################################################################################################
#                                         CONSTANTS                                                 #
#####################################################################################################


BASE_URL = "http://www.bbc.co.uk"
FOLDER_NAME = "recipes-prova"
ERR_FILE = "failed.txt"
TOTAL_NUM = 11298

#####################################################################################################
#                                         FUNCTIONS                                                 #
#####################################################################################################

# TODO: Aggiustare links con os.ppath.join (o simili...)


def rem_underscore(word):
    new_word = ""
    for l in word:
        if l == '_':
            new_word += "%20"
        else:
            new_word += l
    return new_word


def sleep_call(url):
    content = ""
    tries = 1

    while len(content) < 1 and tries <= 10:
        try:
            content = urllib2.urlopen(url).read()
            time.sleep(0.5)
        except urllib2.HTTPError:
            # print "!!!###!!! HTTPERROR !!!###!!!"
            time.sleep(tries * 5)
            if tries == 10:
                errfile = file('..\\{}\\{}'.format(FOLDER_NAME, ERR_FILE), 'w')
                # errfile = open(os.path.join(os.pardir, FOLDER_NAME, ERR_FILE), "w")
                errfile.write(url + '\n')
                errfile.close()

        tries += 1

    return content


def crawler(my_base_url):
    found_recipes = set()
    failed_or_broken = set()

    curr = 0

    num = 0
    food_by_letter_url = "/food/ingredients/by/letter/"
    letters = list(string.ascii_lowercase)

    # for i in re.findall('''href=["'](/food/dishes/by/letter/[a-z])["']''', sleep_call(my_base_url+"/food/dishes", errfile), re.I):
    for l in letters:
        print my_base_url+food_by_letter_url+l
        # [a-z|_\-]+    [\w|-]+
        # print re.findall('''href=["'](/food/[\w\-]+)["']''', sleep_call(my_base_url+food_by_letter_url+l, errfile), re.UNICODE)
        for ee in re.findall('''href=["'](/food/[a-z|_\-]+)["']''', sleep_call(my_base_url+food_by_letter_url+l), re.UNICODE):
            extract = ee[6:]

            ingr = rem_underscore(extract)

            skip = (    ingr == 'seasons' or ingr == 'occasions' or ingr == 'cuisines' or
                        ingr == 'dishes' or ingr == 'techniques' or ingr == 'programmes' or
                        ingr == 'about' or ingr == 'chefs' or ingr == 'ingredients')

            if skip:
                continue

            # print ee

            page = 1
            found = True

            while found:
                found = False
                # [0-9a-z|_\-]+ [\w|-]+

                ingr_query = "http://www.bbc.co.uk/food/recipes/search?page={}&keywords={}".format(page, ingr)

                for recipe in re.findall('''href=["'](/food/recipes/[0-9a-z|_\-]+)["']''', sleep_call(ingr_query), re.UNICODE):
                    # print re.findall('''href=["'](/food/recipes/[\w\-]+)["']''', sleep_call(ingr_query, errfile), re.UNICODE)
                    found = True
                    # print recipe, "found recipes:", len(found_recipes), "ingredient:", ingr, "page:", page

                    response = None
                    tries = 1

                    if recipe in found_recipes:
                        # print "Already found... skip!"
                        continue

                    if recipe in failed_or_broken:
                        # print "Failed or broken... skip!"
                        continue

                    while response is None and tries <= 10:
                        try:
                            response = urllib2.urlopen(my_base_url+recipe)
                            time.sleep(0.5)
                        except urllib2.HTTPError:
                            # print "!!!###!!! HTTPERROR !!!###!!!"
                            time.sleep(tries * 5)
                            if tries == 10:
                                errfile = file('..\\{}\\{}'.format(FOLDER_NAME, ERR_FILE), 'w')
                                # errfile = open(os.path.join(os.pardir, FOLDER_NAME, ERR_FILE), "w")
                                errfile.write(my_base_url+recipe + '\n')
                                errfile.close()
                                failed_or_broken.add(recipe)
                        tries += 1

                    if response is None:
                        continue

                    web_page = response.read()

                    if len(recipe) > 14:
                        name = recipe[14:]
                    else:
                        name = "recipe", num
                        num += 1
                    # print name
                    f = open('..\\{}\\{}.html'.format(FOLDER_NAME, name), 'wt')
                    # print os.path.join(os.path.join(os.pardir, FOLDER_NAME), "{}.html".format(name))
                    # f = open(os.path.join(os.pardir, FOLDER_NAME, "{}.html".format(name)), "wt")
                    f.write(web_page)
                    f.close()

                    found_recipes.add(recipe)

                    curr += 1
                    print "letter {}: found {} of {}".format(l, curr, TOTAL_NUM)

                page += 1


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from utils.utility_functions import ensure_dir
    else:
        from ..utils.utility_functions import ensure_dir

    ensure_dir(FOLDER_NAME)
    crawler(BASE_URL)

