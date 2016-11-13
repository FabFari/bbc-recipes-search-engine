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
    """To extract a recipe out of the corresponding HTML page

        It's used to build a dictionary out of a recipe HTML page,
        extracting only the meaningful information using BeautifulSoup.
        The HTML page is scanned to find all the meaningful HTML tags,
        to obtain from them the meaningful information needed to
        construct the recipe dictionary to be returned.

        :param recipe: The name of the input recipe HTML file
        :return: A Python dict representing the recipe
    """
    f = io.open(os.path.join(os.pardir, RECIPES_DIR, recipe), 'r', encoding='utf-8')
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

    img_url = soup.find_all("img", class_="recipe-media__image responsive-images")
    if len(img_url) > 0:
        img_url = img_url[0]['src']
    else:
        img_url = u''

    dict_recipe['img_url'] = img_url
    # print img_url

    return dict_recipe


def build_corpus():
    """To build a JSON file representing the entire corpus

        It's used to build a JSON made up of recipe JSON objects,
        where each object has a corresponding HTML file that has
        been processed to extract all the meaningful informations
        to be stored in the JSON object put in the corpus file.

        :return: Nothing (void)
    """
    recipes = os.listdir('..\\{}'.format(RECIPES_DIR))
    recipes_list = []

    print "Building Corpus started..."

    tot = len(recipes)
    curr = 1

    for recipe in recipes:
        print 'Now processing "{}", {} of {}.'.format(recipe, curr, tot)
        recipes_list.append(extract_recipe(recipe))
        curr += 1

    with io.open(os.path.join(os.pardir, CORPUS_DIR, CORPUS_NAME), 'wt', encoding='utf-8') as f:
        f.write(unicode(json.dumps(recipes_list, ensure_ascii=False, indent=4, separators=(',', ': '))))

    print "Corpus built."


def check_if_empty(attribute):
    """To check if a recipe attribute is empty

        It's used to check if a specific recipe tag attribute
        extracted from the HTML page of the recipe is empty and
        in this case return an empty unicode string instead.
        Otherwise, if the attribute is not empty, the method
        extracts the text value of the tag and strips from it
        all the whitespace characters.

        :param attribute: The recipe attribute to be tested
        :return: The processed attribute value or the empty unicode string
    """
    if len(attribute) > 0:
        return attribute[0].text.strip()
    else:
        return u''


if __name__ == '__main__':
    from utils.utility_functions import ensure_dir

    ensure_dir(CORPUS_DIR)
    ensure_dir(RECIPES_DIR)
    build_corpus()
