import re
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
from nltk import pos_tag

from utils import unicode_ascii_decoder
from utils.tagger_converter import penn_to_wn
from utils.utility_functions import load_json

RECIPE_JSON = 'recipes.json'

INPUT_DIR = 'data'
OUTPUT_DIR = 'data'

RECIPE_TSV_STEM = 'recipes_stem.tsv'
RECIPE_TSV_LEMM = 'recipes_lemm.tsv'
RECIPE_TSV_TAGS = 'recipes_tags.tsv'
RECIPE_TSV_SNOW = 'recipes_snow.tsv'

DO_STEMMING = "stem"
DO_LEMMIZATION = "lemm"
DO_TAGS_STEMM = "tags"
DO_SNOW_STEMM = "snow"


def process_json_recipes(recipes_file):
    # fl = open('..\\{}\\{}'.format(OUTPUT_DIR, RECIPE_TSV_LEMM), 'wt')
    # fs = open('..\\{}\\{}'.format(OUTPUT_DIR, RECIPE_TSV_STEM), 'wt')
    # ft = open('..\\{}\\{}'.format(OUTPUT_DIR, RECIPE_TSV_TAGS), 'wt')
    fb = open('..\\{}\\{}'.format(OUTPUT_DIR, RECIPE_TSV_SNOW), 'wt')

    recipes = load_json(recipes_file, INPUT_DIR)

    print "Processing JSON..."

    curr = 1
    tot = len(recipes)

    for recipe in recipes:
        print 'Processing recipe "{}": {} of {}'.format(recipe["name"], curr, tot)
        # fl.write(tabularize_recipe(recipe, DO_LEMMIZATION) + '\n')
        # fs.write(tabularize_recipe(recipe, DO_STEMMING) + '\n')
        # ft.write(tabularize_recipe(recipe, DO_TAGS_STEMM) + '\n')
        fb.write(tabularize_recipe(recipe, DO_SNOW_STEMM) + '\n')
        curr += 1

    # fl.close()
    # fs.close()
    # ft.close()
    fb.close()


def prepocess_field(field, process):
    word_tokens = word_tokenize(field)

    # Stopwords removal
    stop_words = set(stopwords.words('english'))
    cleaned_tokens = [w for w in word_tokens if w not in stop_words]

    # Remove punctuation
    no_punct_words = [w for w in cleaned_tokens if not fullmatch('[' + string.punctuation + ']+', w)]

    # Normalization
    uncap_tokens = [w.lower() for w in no_punct_words]

    if process == DO_STEMMING:
        ps = PorterStemmer()
        norm_tokens = [ps.stem(w) for w in uncap_tokens]
    elif process == DO_LEMMIZATION:
        lemmatizer = WordNetLemmatizer()
        norm_tokens = [lemmatizer.lemmatize(w) for w in uncap_tokens]
    elif process == DO_TAGS_STEMM:
        # Tagging
        tagged_tokens = pos_tag(uncap_tokens)
        # Removing conjunctions
        no_conj_tokens = [t for t in tagged_tokens if not t[1] == 'CC']
        lemmatizer = WordNetLemmatizer()
        norm_tokens = [lemmatizer.lemmatize(w[0], penn_to_wn(w[1])) for w in no_conj_tokens]
    else:
        ss = SnowballStemmer('english')
        norm_tokens = [ss.stem(w) for w in uncap_tokens]

    return norm_tokens


def tabularize_recipe(recipe, process):
    recipe_tsv = ""

    process_order = ["name", "title", "descr", "prep_time", "cook_time", "serves",
                     "dietary", "chef", "show", "ingredients", "methods", "img_url"]

    for key in process_order:
        value = recipe[key]
        if key == "name" or key == "img_url" or value == "":
            continue

        if key == "ingredients":
            for val in value:
                if val == "":
                    continue
                decoded_value = unicode_ascii_decoder.unicode_to_ascii(val)
                pp_field = prepocess_field(decoded_value, process)
                recipe_tsv += "III" + "\t"
                recipe_tsv += "\t".join(pp_field) + "\t"
                recipe_tsv += "III" + "\t"

        elif key == "methods":
            for val in value:
                if val == "":
                    continue
                decoded_value = unicode_ascii_decoder.unicode_to_ascii(val)
                pp_field = prepocess_field(decoded_value, process)
                recipe_tsv += "\t".join(pp_field) + "\t"

        elif key == "title":
            decoded_value = unicode_ascii_decoder.unicode_to_ascii(value)
            pp_field = prepocess_field(decoded_value, process)
            recipe_tsv += "TTT" + "\t"
            recipe_tsv += "\t".join(pp_field) + "\t"
            recipe_tsv += "TTT" + "\t"
        else:
            decoded_value = unicode_ascii_decoder.unicode_to_ascii(value)
            pp_field = prepocess_field(decoded_value, process)
            recipe_tsv += "\t".join(pp_field) + "\t"

    return recipe_tsv


def fullmatch(regex, pattern, flags=0):
    """Emulate python-3.4 re.fullmatch()."""
    return re.match("(?:" + regex + r")\Z", pattern, flags=flags)


if __name__ == '__main__':
    from utils.utility_functions import ensure_dir

    ensure_dir(INPUT_DIR)
    ensure_dir(OUTPUT_DIR)
    process_json_recipes(RECIPE_JSON)
