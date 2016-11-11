import os
import json
import operator
from collections import defaultdict

from utils.json_coders import LabeledListDecoder
from utils.json_coders import DocEntryDecoder
from corpus_tokenizer import preprocess_field
from corpus_tokenizer import DO_TAGS_STEMM
from inv_index_builder import TITLE_WEIGHT
from inv_index_builder import ING_WEIGHT


INPUT_DIR = "data"

INDEX_NAME = "inverted_index.json"
JSON_NAME = "documents.json"
TSV_NAME = "recipes_tags.tsv"

THRESHOLD = 0.0
WORDS_STEAK_BONUS = 0.1
PROX_SCORE_FACTOR = 0.5
VEGGIE = "Vegetarian"

# Global Data Structures
dictionary = {}
documents = []


def deunify_dict(d):
    no_utf_d = {}

    for key, value in d.iteritems():
        no_utf_d[str(key)] = value

    return no_utf_d


def load_json_to_str(filename, decoder):
    with open(os.path.join(os.pardir, INPUT_DIR, filename)) as json_data:
        data = json.load(json_data, cls=decoder)

    return deunify_dict(data)


def compute_len_ingr(ing_list, process):
    len_ingr = 0
    print "ing_list: "+str(len(ing_list))
    for ing in ing_list:
        len_ingr += len(preprocess_field(ing, process))
    return len_ingr


def setup_query_engine():
    print 'setup_query_engine..'
    global dictionary
    global documents

    documents = load_json_to_str(JSON_NAME, DocEntryDecoder)
    dictionary = load_json_to_str(INDEX_NAME, LabeledListDecoder)


def perform_query(query, vegetarian=False):
    do_proximity = False

    print 'perform_query..'

    if query[0] == '\"':
        do_proximity = True
        docs = retrieve_docs(query[1:len(query) - 1])
    else:
        docs = retrieve_docs(query)

    res = compute_scores(docs, do_proximity, vegetarian)

    return res


def retrieve_docs(query):
    # Preprocessing query
    print 'Preprocessing query..'

    q_tokenized = preprocess_field(query, DO_TAGS_STEMM)
    q_tokenized = [str(w) for w in q_tokenized]

    retrieved_postings = []
    # i = 0
    print 'retrieving posting lists..'

    for word in q_tokenized:
        # i += 1
        try:
            retrieved_posting = dictionary[word]
        except KeyError:
            continue
        idf = retrieved_posting.get_value()
        if idf > THRESHOLD:
            retrieved_postings.append(retrieved_posting)

    # print i
    return retrieved_postings


# Receive as input the posting lists retrieved
# Compute all the cosine similarities in parallel, returns the top 10
def compute_scores(posting_lists, do_proximity=False, vegetarian=False):
    global documents
    doc_scores = defaultdict(lambda: 0)

    if do_proximity:
        doc_pos = {}
        pair_docs = {}
        prox_score = defaultdict(lambda: 0)

    for cur_list in posting_lists:
        docs = cur_list.get_my_list()
        idf = cur_list.get_value()
        for d in docs:
            doc_id = d.get_label()

            if vegetarian and not documents[doc_id].is_veggie():
                continue
            tf = d.get_value()
            cur_value = doc_scores[doc_id]
            bonus = 0

            if cur_value > 0:
                bonus = WORDS_STEAK_BONUS

            cur_doc = documents[str(doc_id)]
            norm = float(cur_doc.get_size()) + cur_doc.get_title_size()*TITLE_WEIGHT + cur_doc.get_size_ingr()*ING_WEIGHT
            doc_scores[doc_id] = bonus + cur_value + ((tf * idf)/norm)

            if do_proximity:
                if doc_id not in doc_pos.keys():
                    doc_pos[doc_id] = {}
                    doc_pos[doc_id][cur_list.get_label()] = d.get_my_list()
                else:
                    doc_pos[doc_id][cur_list.get_label()] = d.get_my_list()
                if doc_id not in pair_docs.keys():
                    pair_docs[doc_id] = set()
                    pair_docs[doc_id].add((cur_list.get_label(), "NONE"))
                else:
                    pair_docs[doc_id] = extend_pairs(pair_docs[doc_id], cur_list.get_label())

    if do_proximity and len(pair_docs) > 0:
        for doc_id, pairs in pair_docs.iteritems():
            for terms in pairs:
                # print terms
                if terms[1] != "NONE":
                    dist = ev_dist(doc_pos[doc_id][terms[0]], doc_pos[doc_id][terms[1]])
                    if dist < terms and dist != 0:
                        prox_score[doc_id] += PROX_SCORE_FACTOR*(1 / dist)
            try:
                doc_scores[doc_id] += prox_score[doc_id]
            except KeyError:
                continue

    if vegetarian:
        veggie_docs = {doc_id: score for doc_id, score in doc_scores.iteritems() if documents[doc_id].is_veggie()}
        ordered_docs = sorted(veggie_docs.items(), key=operator.itemgetter(1), reverse=True)
    else:
        ordered_docs = sorted(doc_scores.items(), key=operator.itemgetter(1), reverse=True)

    res = [documents[str(doc_pair[0])] for doc_pair in ordered_docs[:10]]

    return res


def extend_pairs(pair_docs, doc_id):
    new_pairs = set()

    for p in pair_docs:
        new_pairs.add((p[0], doc_id))
        if p[1] != "NONE":
            new_pairs.add((p[1], doc_id))

    return new_pairs


def ev_dist(pos_list_i, pos_list_j):
    min_dist = abs(pos_list_i[0] - pos_list_j[0])

    for p_i in pos_list_i:
        for p_j in pos_list_j:
            dist = abs(p_i - p_j)
            if dist < min_dist:
                min_dist = dist
            if p_j > p_i:
                break

    return min_dist


if __name__ == '__main__':
    from utils.utility_functions import ensure_dir

    ensure_dir(INPUT_DIR)
    setup_query_engine()

    while True:
        user_in = raw_input("Ask user for something.")
        result = perform_query(user_in)
        result = [w.get_name() for w in result]
        print result
