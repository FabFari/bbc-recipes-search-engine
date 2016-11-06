import io
import re
import os
import json
from collections import OrderedDict
from bs4 import BeautifulSoup

RECIPES_DIR = "recipes"
CORPUS_DIR = "data"
CORPUS_NAME = "recipes.json"


def extract_recipe(recipe):
    f = io.open('..\\{}\\{}'.format(RECIPES_DIR, recipe), 'r', encoding='utf-8')
    soup = BeautifulSoup(f, 'html5lib')
    # dict_recipe = dict()
    dict_recipe = OrderedDict()

    # Single elements
    dict_recipe["name"] = recipe.rsplit(".html")[0]
    # print recipe.rsplit(".html")[0]
    title = check_if_empty(soup.find_all("h1", class_='content-title__text'))
    dict_recipe["title"] = title
    # print "Title:", title
    descr = check_if_empty(soup.find_all("p", class_='recipe-description__text'))
    dict_recipe["descr"] = descr
    # print "Description:", descr

    prep_time = check_if_empty(soup.find_all("p", class_='recipe-metadata__prep-time'))
    dict_recipe["prep_time"] = prep_time
    # print "Preparation Time:", prep_time

    cook_time = check_if_empty(soup.find_all("p", class_='recipe-metadata__cook-time'))
    dict_recipe["cook_time"] = cook_time
    # print "Cooking Time:", cook_time

    serves = check_if_empty(soup.find_all("p", class_='recipe-metadata__serving'))
    dict_recipe["serves"] = serves
    # print "Servings:", serves

    dietary = check_if_empty(soup.find_all("div", class_='recipe-metadata__dietary'))
    dict_recipe["dietary"] = dietary

    chef_about = soup.find_all("a", class_='chef__link')

    if len(chef_about) > 1:
        chef = chef_about[0].text.strip()
        show = chef_about[1].text.strip()
    else:
        chef = check_if_empty(chef_about)
        show = u''

    dict_recipe["chef"] = chef
    # print "Chef:", chef

    dict_recipe["show"] = show
    # print "Show:", show

    # ingredients = get_list(soup.find_all("li", class_='recipe-ingredients__list-item'))
    ingredients = [elem.get_text() for elem in soup.select("li.recipe-ingredients__list-item")]
    # print "Ingredients: ", ingredients
    dict_recipe["ingredients"] = ingredients

    methods = [re.sub('\s{2,}', '', elem.get_text()) for elem in soup.select("li.recipe-method__list-item")]
    dict_recipe["methods"] = methods
    # print "Methods: ", methods

    return dict_recipe


def build_corpus():
    recipes = os.listdir('..\\{}'.format(RECIPES_DIR))
    recipes_list = []

    print "Building Corpus started..."

    tot = len(recipes)
    curr = 1

    for recipe in recipes:
        print 'Now processing "{}", {} of {}.'.format(recipe, curr, tot)
        recipes_list.append(extract_recipe(recipe))
        curr += 1

    with io.open('..\\{}\\{}'.format(CORPUS_DIR, CORPUS_NAME), 'wt', encoding='utf-8') as f:
        f.write(unicode(json.dumps(recipes_list, ensure_ascii=False, indent=4, separators=(',', ': '))))

    print "Corpus built."


def check_if_empty(attribute):
    if len(attribute) > 0:
        return attribute[0].text.strip()
    else:
        return u''


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from utils.utility_functions import ensure_dir
    else:
        from ..utils.utility_functions import ensure_dir

    ensure_dir(CORPUS_DIR)
    ensure_dir(RECIPES_DIR)
    build_corpus()
