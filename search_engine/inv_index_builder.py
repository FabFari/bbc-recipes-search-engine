import csv
import json
import math

INPUT_DIR = "data"
OUTPUT_DIR = "data"

TSV_NAME = "recipes_tags.tsv"
INDEX_NAME = "inverted_index.json"
TITLE_WEIGHT = 10
ING_WEIGHT = 3

INGR_NEG_OFFSET = -1000

doc_number = 0


def build_index_json(tsv=None, filename=None):
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from utils.utility_functions import load_tsv
    from utils.json_coders import LabeledListEncoder

    if tsv:
        inv_index = sort_entries(collect_terms(load_tsv(tsv, INPUT_DIR)))
    else:
        inv_index = sort_entries(collect_terms(load_tsv(TSV_NAME, INPUT_DIR)))

    if not filename:
        filename = INDEX_NAME
    print 'Writing in json file...'
    with open("..\\{}\\{}".format(OUTPUT_DIR, filename), "wt") as f:
        f.write(json.dumps(inv_index, indent=4, separators=(',', ': '), cls=LabeledListEncoder))
    print 'Write done'


def process_corpus(tsv=None):
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from utils.utility_functions import load_tsv

    if tsv:
        return sort_entries(collect_terms(load_tsv(tsv, INPUT_DIR)))
    return sort_entries(collect_terms(load_tsv(TSV_NAME, INPUT_DIR)))


def collect_terms(list_of_lists):
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from utils.data_structures import ParsedEntry

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
            if t == 'TTT':
                title = not title
            elif t == 'III':
                ing = not ing
            else:
                if title:
                    entry = ParsedEntry(t, doc_id, -doc_pos)
                elif ing:
                    entry = ParsedEntry(t, doc_id, INGR_NEG_OFFSET - doc_pos)
                else:
                    entry = ParsedEntry(t, doc_id, doc_pos)

                terms.append(entry)
                doc_pos += 1
        doc_id += 1

    doc_number = doc_id + 1
    print 'Terms collected...'
    return terms


def sort_entries(list_pe):
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from utils.data_structures import LabeledList

    print 'Building index...'
    parsed_entries = sorted(list_pe, key=lambda parsed_entry: parsed_entry.term)
    num_entries = len(parsed_entries)

    dictionary = {}
    index = 0
    while index < num_entries:
        current_term = parsed_entries[index].get_term()
        term_dictionary = []
        print 'term {} of {}'.format(index, num_entries)

        while index < num_entries and parsed_entries[index].get_term() == current_term:
            current_doc_id = parsed_entries[index].get_doc_id()
            position_list = []
            title = 0
            ing = 0
            occurs = 1
            while index < num_entries and\
                    parsed_entries[index].get_term() == current_term and\
                    parsed_entries[index].get_doc_id() == current_doc_id:

                # To cumulate weight of repeated words
                pos = parsed_entries[index].get_doc_position()
                if pos <= -1000:
                    ing += 1/occurs
                    parsed_entries[index].set_doc_position(-(pos + 1000))
                elif pos <= 0:
                    title += 1/occurs
                    parsed_entries[index].set_doc_position(-pos)

                position_list.append(parsed_entries[index].get_doc_position())

                index += 1
                occurs += 1

            tf_td = math.log10(1.0 + len(position_list) + title*TITLE_WEIGHT + ing*ING_WEIGHT)
            # We could compute tf*idf directly here
            term_doc_entry = LabeledList(current_doc_id, position_list, tf_td)
            term_dictionary.append(term_doc_entry)

        idf = math.log10((float(doc_number) / len(term_dictionary)))
        entry_dict = LabeledList(current_term, term_dictionary, idf)
        dictionary[current_term] = entry_dict

    print 'Index built'
    return dictionary

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
    build_index_json()
