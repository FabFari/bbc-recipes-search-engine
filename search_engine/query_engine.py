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
# File name of the inverted index
INDEX_NAME = "inverted_index.json"
# File name of the collection of documents
JSON_NAME = "documents.json"

TSV_NAME = "recipes_tags.tsv"

# Term-Document 's with an idf score < THRESHOLD will be ignored
THRESHOLD = 0.0
# Documents with many query terms will have their score boosted
WORDS_STEAK_BONUS = 0.1
PROX_SCORE_FACTOR = 0.5

# Number of query results to be returned
K = 10

# To test vegetarian documents
VEGGIE = "Vegetarian"

# Global Data Structures
dictionary = {}
documents = []


def deunify_dict(d):
    """To transform a unicode keyed dict into an ASCII keyed one

        It's used to convert the result of the json.load() method
        when called on a unicode file, that is a unicode keyed dict
        in our case, to a more manageable ASCII keyed dict.
        All the unicode keys are converted to ASCII while the values
        of the specific keys stays unchanged.

        :param d: The unicode keyed dict to be processed
        :return: The ASCII keyed dict result of the process
    """
    no_utf_d = {}

    for key, value in d.iteritems():
        no_utf_d[str(key)] = value

    return no_utf_d


def load_json_to_str(filename, decoder):
    """To load data from a JSON file with a custom JSONDecoder

        It's used to load the data read from a JSON file that
        what previously encoded by a custom JSONEncoder class.
        It's able to read the data and automatically produce
        the specific Python object of the class specified into
        the JSON object, using a custom JSONDecoder class
        specified in the call of json.load() method. It basically
        act as a wrapper for the calling of this latter function.
        Then, in the end it also bundles the call to the method
        deunify_dict(), to return to the caller an ASCII keyed dict.

        :param filename: The name of the JSON file to be loaded
        :param decoder: The name of the JSONDecoder class to use
        :return: The data loaded from the JSON file
    """
    with open(os.path.join(os.pardir, INPUT_DIR, filename)) as json_data:
        data = json.load(json_data, cls=decoder)

    return deunify_dict(data)


def setup_query_engine():
    """To load in memory all the data structures needed by the query engine

        It's used to load in memory all the data structures needed by the
        query engine to support the execution of queries.
        The data structures to be loaded in memory are:
            - The inverted index, that is stored in JSON file and that
              must be loaded into memory to perform the query;
            - The document dictionary, containing useful information about the
              documents (e.g. name, title, exc.) needed both to support the query
              execution (e.g. title_size) and to effectively provide results to
              the users (e.g. desc, img_url).

        :return: Nothing (void)
    """
    print 'setup_query_engine...'
    global dictionary
    global documents

    documents = load_json_to_str(JSON_NAME, DocEntryDecoder)
    dictionary = load_json_to_str(INDEX_NAME, LabeledListDecoder)


def perform_query(query, vegetarian=False):
    """To wrap the processing of a user submitted query

        It's used to wrap the entire processing of any
        user submitted query to the query engine.
        It glues together two core processes:
            - The retrieval of the relevant posting lists
             (i.e. one for each relevant query term)
            - The scoring of all the documents contained
              in the posting lists and the retrieval of
              the top K scored documents in the result

        :param query: The query submitted by the user
        :param vegetarian: To specify if the query is vegetarian or no
        :return: The top K scored documents found
    """
    do_proximity = False

    print 'perform_query...'

    if query[0] == '\"':
        do_proximity = True
        docs = retrieve_docs(query[1:len(query) - 1])
    else:
        docs = retrieve_docs(query)

    res = compute_scores(docs, do_proximity, vegetarian)

    return res


def retrieve_docs(query):
    """To retrieve all the documents containing query terms.

        It's used to retrieve the existing posting lists
        for the query terms, in order to obtain all the
        relevant documents for the query itself.
        Before doing that, the query is pre-processed in
        the same way as the documents, in order to obtain
        tokens and to obtain the posting lists of those
        if they exists in the inverted index.
        Furthermore, the set of meaningful posting lists
        can be filtered, to get rid of those terms with
        too smaller IDF values by a user tunable threshold.

        :param query: The query submitted by the user
        :return: The posting list retrieved
    """
    # Preprocessing query
    print 'Preprocessing query..'

    q_tokenized = preprocess_field(query, DO_TAGS_STEMM)
    q_tokenized = [str(w) for w in q_tokenized]

    retrieved_postings = []
    # i = 0
    print 'retrieving posting lists..'

    # For each word in the processed query
    # Retrieve the corresponding posting list.
    for word in q_tokenized:
        # i += 1
        try:
            retrieved_posting = dictionary[word]
        except KeyError:
            continue
        idf = retrieved_posting.get_value()
        # idf scores < THRESHOLD will be ignored
        if idf > THRESHOLD:
            retrieved_postings.append(retrieved_posting)

    return retrieved_postings


# Receiving as input the posting lists retrieved,
# this method is to be used to compute the relevance, with respect to the query, of the documents retrieved.
# The method is called for each query and returns the top 10 scoring documents.
# Documents' scores are computed in parallel;
# The specific term-document tf idf are already precomputed.
def compute_scores(posting_lists, do_proximity=False, vegetarian=False):
    """To return the top K scored documents of the query

        It's used to compute the relevance, with respect to the
        query, of the documents retrieved, contained in the input
        posting list output of the previous step process.
        Documents' scores are computed in parallel, with the
        posting list explored sequentially (term-at-the-time).
        The score is calculated using the conventional TF-IDF
        mechanism, where the specific term-document TF and
        IDF are already precomputed to save time at runtime.
        Moreover, additional steps are required if the query:
            - Is a 'phrase query', and in this case the position
              lists contained in the document entries of the
              posting list needs to be processed to calculate
              the bonus derived by the position of query terms
              within the posting list documents.
            - Is a 'vegetarian query', and in this case the list
              of relevant documents must be filtered to find only
              those that are marked as 'Vegetarian'.

        :param posting_lists: The list of input posting lists
        :param do_proximity: To specify if is a phrase query or not
        :param vegetarian: To specify if is a vegetarian query or not
        :return: The top K scored documents of the query
    """
    global documents
    doc_scores = defaultdict(lambda: 0)

    # Structures needed to perform phrase queries
    if do_proximity:
        # Data structure containing all the position lists for each document in the
        # posting lists, for all the query terms contained in that specific document
        # (i.e. doc_pos[doc_id][t] := position list for term t in of document doc_id)
        doc_pos = {}
        # Data structure containing all the possible C(n,2) (i.e. term pairs)
        # combinations of the query terms contained the document (n in total)
        # for all the documents in the posting lists
        pair_docs = {}
        # Dictionary keeping the additional proximity score for the documents
        prox_score = defaultdict(lambda: 0)

    # Compute the score for each document appearing in any of the posting lists retrieved
    for cur_list in posting_lists:
        docs = cur_list.get_my_list()
        idf = cur_list.get_value()
        
        # For each document in the current posting list,
        # Retrieve the tf and idf scores
        # Compute the norm taking into account the length and the weight of the different parts of the document
        # The vegetarian flag, if set, filter out all the non vegetarian results.
        # The do_proximity flag, if set, perform phrase queries
        for d in docs:
            doc_id = d.get_label()

            if vegetarian and not documents[str(doc_id)].is_veggie():
                continue
            tf = d.get_value()
            cur_value = doc_scores[doc_id]
            bonus = 0

            # Fabri come dicevi ieri tu dovremmo toglierlo questo bonus ora.
            if cur_value > 0:
                bonus = WORDS_STEAK_BONUS

            cur_doc = documents[str(doc_id)]
            norm = float(cur_doc.get_size()) + cur_doc.get_title_size()*TITLE_WEIGHT + cur_doc.get_size_ingr()*ING_WEIGHT
            doc_scores[doc_id] = bonus + cur_value + ((tf * idf)/norm)

            # Here phrase queries relevant data structures are populated.
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

    # Here proximity scores for all the documents are calculated
    if do_proximity and len(pair_docs) > 0:
        for doc_id, pairs in pair_docs.iteritems():
            for terms in pairs:
                if terms[1] != "NONE":
                    # The minimum distance between each pair of query term
                    # contained in the document is used as a an indicator
                    # of the term proximity in evaluating the phrase query
                    dist = ev_dist(doc_pos[doc_id][terms[0]], doc_pos[doc_id][terms[1]])
                    # I'm interested only in the distances that are smaller than the query length
                    if dist < terms and dist != 0:
                        prox_score[doc_id] += PROX_SCORE_FACTOR*(1 / dist)
            try:
                doc_scores[doc_id] += prox_score[doc_id]
            except KeyError:
                continue

    # Order the results in descending order of their score.
    if vegetarian:
        veggie_docs = {str(doc_id): score for doc_id, score in doc_scores.iteritems() if documents[str(doc_id)].is_veggie()}
        ordered_docs = sorted(veggie_docs.items(), key=operator.itemgetter(1), reverse=True)
    else:
        ordered_docs = sorted(doc_scores.items(), key=operator.itemgetter(1), reverse=True)

    res = [documents[str(doc_pair[0])] for doc_pair in ordered_docs[:K]]

    return res


def extend_pairs(pair_docs, term):
    """To extend the input set of term pairs with a new term

        It's used to extend the set of term pairs with a new term
        taking into account the duplicates (by using a set).
        If the input pair_docs set is empty, the resulting set is
        made of a pair of one term and a wildcard ('NONE'), that
        is trashed in subsequent call of the method on that set.

        :param pair_docs: The set of terms pairs currently calculated
        :param term: The term to be added to the current set of pairs
        :return: The new set of term pairs extended with the new term
    """
    new_pairs = set()

    for p in pair_docs:
        new_pairs.add((p[0], term))
        if p[1] != "NONE":
            new_pairs.add((p[1], term))

    return new_pairs


def ev_dist(pos_list_i, pos_list_j):
    """To evaluate the minimum distance between two term position lists

        It's used to calculate the minimum distance between
        each pair of positions (i,j), with position i belonging
        to pos_list_i and position j belonging to pos_list_j.
        In this case, the minimum position between the two
        terms is used as an indicator of the proximity score
        between the terms associated to the position lists
        in the document the position lists belongs to.

        :param pos_list_i: The first position list
        :param pos_list_j: The second position list
        :return: The minimum distance between the two term position lists
    """
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
