import json
import timeit
import operator
from collections import defaultdict
from corpus_tokenizer import prepocess_field
from corpus_tokenizer import DO_TAGS_STEMM


INPUT_DIR = "data"

INDEX_NAME = "inverted_index.json"
JSON_NAME = "recipes.json"
TSV_NAME = "recipes_lemm.tsv"

THRESHOLD = 0.0
WORDS_STEAK_BONUS = 0.1

# Global Data Structures
dictionary = {}
documents = []


def deunify_dict(d):
    no_utf_d = {}

    for key, value in d.iteritems():
        no_utf_d[str(key)] = value

    return no_utf_d


def load_json_to_str(filename=None):
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from utils.json_coders import LabeledListDecoder

    if not filename:
        filename = INDEX_NAME
    with open("..\\{}\\{}".format(INPUT_DIR, filename)) as json_data:
        data = json.load(json_data, cls=LabeledListDecoder)

    return deunify_dict(data)


def setup_query_engine():
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from utils.data_structures import DocEntry
    from utils.utility_functions import load_tsv
    from utils.utility_functions import load_json

    print 'setup_query_engine..'
    global dictionary
    global documents

    docs_list = load_tsv(TSV_NAME, INPUT_DIR)
    doc_jsons = load_json(JSON_NAME, INPUT_DIR)

    curr_id = 0
    for d in docs_list:
        documents.append(DocEntry(curr_id, doc_jsons[curr_id]["name"], len(d)))
        curr_id += 1

    dictionary = load_json_to_str()


def perform_query(query):
    print 'perform_query..'

    docs = retrieve_docs(query)
    res = compute_scores(docs)
    doc_list = [str(documents[doc[0]].get_name()) for doc in res]
    return doc_list


def retrieve_docs(query):
    # Preprocessing query
    print 'Preprocessing query..'

    q_tokenized = prepocess_field(query, DO_TAGS_STEMM)
    q_tokenized = [str(w) for w in q_tokenized]

    retrieved_postings = []
    i = 0
    print 'retrieving posting lists..'

    for word in q_tokenized:
        i += 1
        try:
            retrieved_posting = dictionary[word]
        except:
            continue
        idf = retrieved_posting.get_value()
        if idf > THRESHOLD:
            retrieved_postings.append(retrieved_posting)

    #print i
    return retrieved_postings


# Receive as input the posting lists retrieved
# Compute all the cosine similarities in parallel, returns the top 10
def compute_scores(posting_lists):
    global documents
    doc_scores = defaultdict(lambda: 0)

    for cur_list in posting_lists:
        docs = cur_list.get_my_list()
        idf = cur_list.get_value()
        for d in docs:
            doc_id = d.get_label()
            tf = d.get_value()
            cur_value = doc_scores[doc_id]
            bonus = 0

            if cur_value > 0:
                bonus = WORDS_STEAK_BONUS

            doc_scores[doc_id] = bonus + cur_value + ((tf * idf)/float(documents[doc_id].get_size()))

    ordered_docs = sorted(doc_scores.items(), key=operator.itemgetter(1), reverse=True)
    return ordered_docs[:20]


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from utils.utility_functions import ensure_dir
    else:
        from ..utils.utility_functions import ensure_dir

    ensure_dir(INPUT_DIR)
    setup_query_engine()

    while True:
        user_in = raw_input("Ask user for something.")
        doc_list = perform_query(user_in)
        print doc_list
