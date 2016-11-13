import os
import re
import string
import json

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
from nltk import pos_tag

from utils import unicode_ascii_decoder
from utils.tagger_converter import penn_to_wn
from utils.utility_functions import load_json
from utils.data_structures import DocEntry
from utils.json_coders import DocEntryEncoder

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

DOCUMENTS = "documents.json"


def process_name(process):
    """To decide the name of file output of the process

        It's used to decide the name of the file created at the
        end of the pre-processing process. The name is decided
        accordingly with the specific preprocessing process applied
        to the documents, according the constants based mechanism
        listed at the beginning of the Python file.

        :param process: The name of the pre-processing process to be executed
        :return: The name of the TSV file result of the process
    """
    if process == DO_STEMMING:
        return RECIPE_TSV_STEM
    elif process == DO_LEMMIZATION:
        return RECIPE_TSV_LEMM
    elif process == DO_TAGS_STEMM:
        return RECIPE_TSV_TAGS
    else:
        return RECIPE_TSV_SNOW


def process_json_recipes(recipes_file=None, process=None):
    """To pre-process the corpus JSON file

        It's used to run the pre-processing step on each document
        stored within the corpus JSON file. Each recipe JSON object
        is read from the file, pre-processed and then stored in a
        specific TSV file, containing a row for each document.
        The process also produces another file to support the query
        execution and presentation at runtime.

        :param recipes_file: The name of the corpus JSON file
        :param process: The name of the pre-processing step to execute
        :return: Nothing (void)
    """
    if not recipes_file:
        recipes_file = RECIPE_JSON

    if not process:
        process = DO_TAGS_STEMM

    f = open(os.path.join(os.pardir, OUTPUT_DIR, process_name(process)), 'wt')

    recipes = load_json(recipes_file, INPUT_DIR)

    print "Processing JSON..."

    tot = len(recipes)
    documents = {}
    i = 0
    for recipe in recipes:
        print 'Processing recipe "{}": {} of {}'.format(recipe["name"], i + 1, tot)
        f.write(tabularize_recipe(recipe, process, i, documents=documents) + '\n')
        i += 1

    f.close()

    # write json documents
    with open("..\\{}\\{}".format(OUTPUT_DIR, DOCUMENTS), "wt") as f:
        f.write(json.dumps(documents, indent=4, separators=(',', ': '), cls=DocEntryEncoder))


def preprocess_field(field, process):
    """To pre-process a single recipe document field

        It's used to pre-process a single field of a
        recipe document. The pre-processing steps are:
        - Tokenization
        - Stop-Words removal
        - Punctuation removal
        - Case normalization
        - One of the available lemmatization/stemming processes:
            - Porter Stemmer stemming
            - NLTK default lemmatizer lemmatization
            - WordNet lemmatizer lemmatization
            - Snowball Stemmer stemming
        The result of the whole process is an iterable list of
        tokens went through all the pre-process steps.

        :param field: The recipe field to be pre-processed
        :param process: The pre-process step to execute
        :return: An iterable list of tokens
    """
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


def tabularize_recipe(recipe, process, doc_id, documents=None):
    """To produce a tab-separated document starting from a recipe document

        It's used to produce, starting from the recipe document
        dictionary, a single line tab-separated document to be stored
        in the TSV file representing the entire pre-processed corpus.
        The method also extract other information out of the input
        recipe document, to support the query execution and presentation
        at runtime, temporarily stored in the variable 'documents'


        :param recipe: The input recipe document represent as a dict
        :param process: The pre-processing process to execute
        :param doc_id: The id of the recipe document to process
        :param documents: The dictionary with query support information
        :return: The single line tab-separated representation of the recipe
    """
    recipe_tsv = ""

    process_order = ["name", "title", "descr", "prep_time", "cook_time", "serves",
                     "dietary", "chef", "show", "ingredients", "methods", "img_url"]
    size_doc = 0
    de = DocEntry(id=doc_id)

    for key in process_order:
        value = recipe[key]

        if value == "":
            continue

        elif key == "name":
            de.set_name(value)

        elif key == "img_url":
            de.set_img_url(value)

        elif key == "ingredients":
            for val in value:
                if val == "":
                    continue
                decoded_value = unicode_ascii_decoder.unicode_to_ascii(val)
                pp_field = preprocess_field(decoded_value, process)
                de.set_size_ingr(de.get_size_ingr() + len(pp_field))
                size_doc += len(pp_field)

                recipe_tsv += "III" + "\t"
                recipe_tsv += "\t".join(pp_field) + "\t"
                recipe_tsv += "III" + "\t"

        elif key == "methods":
            for val in value:
                if val == "":
                    continue
                decoded_value = unicode_ascii_decoder.unicode_to_ascii(val)
                pp_field = preprocess_field(decoded_value, process)
                recipe_tsv += "\t".join(pp_field) + "\t"
                size_doc += len(pp_field)

        elif key == "title":
            decoded_value = unicode_ascii_decoder.unicode_to_ascii(value)
            pp_field = preprocess_field(decoded_value, process)
            de.set_title(value)
            de.set_title_size(len(pp_field))
            size_doc += len(pp_field)

            recipe_tsv += "TTT" + "\t"
            recipe_tsv += "\t".join(pp_field) + "\t"
            recipe_tsv += "TTT" + "\t"

        elif key == "descr":
            decoded_value = unicode_ascii_decoder.unicode_to_ascii(value)
            pp_field = preprocess_field(decoded_value, process)
            recipe_tsv += "\t".join(pp_field) + "\t"
            de.set_desc(value)
            size_doc += len(pp_field)

        elif key == "dietary" and value == "Vegetarian":
            decoded_value = unicode_ascii_decoder.unicode_to_ascii(value)
            pp_field = preprocess_field(decoded_value, process)
            recipe_tsv += "\t".join(pp_field) + "\t"
            de.set_veggie(True)
            size_doc += len(value)

        else:
            decoded_value = unicode_ascii_decoder.unicode_to_ascii(value)
            pp_field = preprocess_field(decoded_value, process)
            recipe_tsv += "\t".join(pp_field) + "\t"
            size_doc += len(pp_field)

    de.set_size(size_doc)

    if documents is not None:
        documents[doc_id] = de

    return recipe_tsv


def fullmatch(regex, pattern, flags=0):
    """To Emulate python-3.4 re.fullmatch() method

        To emulate the behaviour of the Python 3.4 specific
        re.fullmatch() method in Python 2.7.X.
        The method is used to efficiently remove the punctuation
        when pre-processing the recipe documents

        :param regex: The regular expression to be matched
        :param pattern: The pattern the regular expression has to match
        :param flags: Optional flags to the process
        :return: The corresponding matching object

    """
    return re.match("(?:" + regex + r")\Z", pattern, flags=flags)


if __name__ == '__main__':
    from utils.utility_functions import ensure_dir

    ensure_dir(INPUT_DIR)
    ensure_dir(OUTPUT_DIR)
    process_json_recipes(RECIPE_JSON, DO_TAGS_STEMM)
