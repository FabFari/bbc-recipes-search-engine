import os
import json
import math

from utils.utility_functions import load_tsv
from utils.json_coders import LabeledListEncoder
from utils.data_structures import ParsedEntry
from utils.data_structures import LabeledList

INPUT_DIR = "data"
OUTPUT_DIR = "data"

TSV_NAME = "recipes_tags.tsv"

# Name of the file where the inverted index will be stored
INDEX_NAME = "inverted_index.json"

# How much words in the title will be weighted compared to words in the recipe description
TITLE_WEIGHT = 10

# How much words in the ingredients will be weighted compared to words in the recipe description
ING_WEIGHT = 3

# This value is the result of the assumption that no title is longer than 999 words
INGR_NEG_OFFSET = -1000

# The doc IDs will start from 0
doc_number = 0


# This method orchestrates the construction of the posting lists from the corpus,
# It then writes the result in a json file.
def build_index_json(tsv=None, filename=None):
    """To wrap the entire index building process and store

        It's used to wrap the entire process to build the inverted
        index out of the TSV corpus file and then to store it in
        a file to be then loaded at runtime.
        The index is written to a file by the means of a custom
        JSONEncoder class exploited by the method json.dumps(),
        so that at loading time the corresponding Python object
        will be automatically reconstructed using the matching
        JSONDecoder class in support to the loading process.

        :param tsv: The name of the TSV file of the pre-processed corpus
        :param filename: The name of the file where the inverted index will be stored
        :return: Nothing (void)
    """
    if tsv:
        inv_index = sort_entries(collect_terms(load_tsv(tsv, INPUT_DIR)))
    else:
        inv_index = sort_entries(collect_terms(load_tsv(TSV_NAME, INPUT_DIR)))

    if not filename:
        filename = INDEX_NAME
    print 'Writing in json file...'
    with open(os.path.join(os.pardir, OUTPUT_DIR, filename), "wt") as f:
        f.write(json.dumps(inv_index, indent=4, separators=(',', ': '), cls=LabeledListEncoder))
    print 'Write done'


def collect_terms(list_of_lists):
    """To collect the terms from the TSV file loaded in memory

        It's used to collect all the terms out of the entire TSV
        corpus file, loaded in memory as a list (the documents)
        of list of tokens (the list of tokens for that document).
        The documents are processed one at a time and each term
        contained into the document is added to the list of
        of terms currently collected as a ParsedEntry object.
        This object maintains the information related to the
        document the term belonged and its position within it.
        Furthermore, the method also identifies the portions of
        the document representing the title (delimited by TTT tokens)
        and the ingredients (delimited by III tokens). This is
        required because this portions of the document has to
        be assigned with a specific weighted score later on.

        :param list_of_lists: The list of token lists for each document
        :return: The list of terms collected over all the documents
    """
    global doc_number
    terms = []
    doc_id = 0
    doc_num = len(list_of_lists)
    print 'Collecting terms...'
    for doc in list_of_lists:
        doc_pos = 0
        print 'doc {} of {}'.format(doc_id, doc_num)

        title = False
        ing = False
        for t in doc:
            # The code TTT is used to delimit words in the title
            if t == 'TTT':
                title = not title
            # The code III is used to delimit words in the title
            elif t == 'III':
                ing = not ing
            # Creates an Entry with the information obtained
            else:
                if title:
                    entry = ParsedEntry(t, doc_id, -doc_pos)
                elif ing:
                    entry = ParsedEntry(t, doc_id, INGR_NEG_OFFSET - doc_pos)
                else:
                    entry = ParsedEntry(t, doc_id, doc_pos)

                # Add the term to the structure and advance
                terms.append(entry)
                doc_pos += 1
        # Assign a new key to the next document
        doc_id += 1

    doc_number = doc_id + 1
    print 'Terms collected...'
    return terms


def sort_entries(list_pe):
    """To build the posting lists and then the inverted index

        It's used to build the posting lists starting from the list
        of terms collected from the documents in the previous step.
        Starting from the collection of terms, these are sorted
        in alphabetical to facilitate the processing operation.
        During the process:
            - The posting lists for each distinct term are built:
              for each document containing the term, a LabeledList
              object is created, storing the TF (term frequency) for
              that document and the term position list. This frequency
              is weighted and normalized properly, with title
              and ingredients terms obtaining different weights.
            - The term IDF is computed looking at all the terms
              repetition within the documents: since the collection
              is sorted, the same terms will be consecutive in the
              collection, making this step very efficient.
        The posting lists are arranged into a term keyed Python dict,
        in order to access the posting list efficiently.

        :param list_pe: The name of the TSV file of the pre-processed corpus
        :return: The inverted index represented as a dictionary of posting lists
    """
    print 'Building index...'
    parsed_entries = sorted(list_pe, key=lambda parsed_entry: parsed_entry.term)
    num_entries = len(parsed_entries)

    dictionary = {}
    index = 0
    # For each term read from the ordered list of words received
    while index < num_entries:
        current_term = parsed_entries[index].get_term()
        term_dictionary = []
        print 'term {} of {}'.format(index, num_entries)

        # Until the term read is the same
        while index < num_entries and parsed_entries[index].get_term() == current_term:
            current_doc_id = parsed_entries[index].get_doc_id()
            position_list = []
            title = 0
            ing = 0
            # For implementing a basic spam control mechanism (disabled by default)
            # Occurrences counter: needed for spam control in
            # title and ingredients weighting.
            # occurs = 1
            
            # For each occurrence of the current term in the same document
            while index < num_entries and\
                    parsed_entries[index].get_term() == current_term and\
                    parsed_entries[index].get_doc_id() == current_doc_id:

                # To cumulate weight of repeated words
                pos = parsed_entries[index].get_doc_position()
                # According to our structures:
                # all the positions < -1000 are reserved for ingredients
                if pos <= -1000:
                    ing += 1
                    # If the word-steak bonus is active (disabled as default):
                    # ing += 1/occurs
                    parsed_entries[index].set_doc_position(-(pos + 1000))
                # all the positions -1000< x < 0 are reserved for the words in the title
                elif pos <= 0:
                    title += 1
                    # If the word-steak bonus is active (disabled as default):
                    # title += 1/occurs
                    parsed_entries[index].set_doc_position(-pos)

                # Store all the positions of the occurrences of the term in the document
                position_list.append(parsed_entries[index].get_doc_position())
                # Read new line
                index += 1
                # For implementing a basic spam control mechanism (disabled by default)
                # Increments occurrences counter
                # occurs += 1

            # Compute the term frequency in the current document weighting differently different parts of the document
            tf_td = math.log10(1.0 + len(position_list) + title*TITLE_WEIGHT + ing*ING_WEIGHT)
            # Create an object containing the tf score and the occurrences of the term in the document
            term_doc_entry = LabeledList(current_doc_id, position_list, tf_td)
            # Append the object to the current posting list
            term_dictionary.append(term_doc_entry)
            
        # Compute the inverse document frequency
        idf = math.log10((float(doc_number) / len(term_dictionary)))
        # Create and insert in the dict the posting list of "current_term" with the corresponding documents and idf.
        entry_dict = LabeledList(current_term, term_dictionary, idf)
        dictionary[current_term] = entry_dict

    print 'Index built'
    return dictionary

if __name__ == '__main__':
    from utils.utility_functions import ensure_dir

    ensure_dir(INPUT_DIR)
    ensure_dir(OUTPUT_DIR)
    build_index_json()
