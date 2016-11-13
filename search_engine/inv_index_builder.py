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
#Name of the file where the inverted index will be store
INDEX_NAME = "inverted_index.json"
#How much words in the title will be weighted compared to words in the recipe description
TITLE_WEIGHT = 10
#How much words in the ingredients will be weighted compared to words in the recipe description
ING_WEIGHT = 3
#This value is the result of the assuption that no title is longer than 999 words
INGR_NEG_OFFSET = -1000
#The doc IDs will start from 0
doc_number = 0

#This method orchestrates the construction of the posting lists from the corpus, 
#It then writes the result in a json file.
def build_index_json(tsv=None, filename=None):
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

#NON VIENE GIÀ FATTO DAL METODO SOPRA?
def process_corpus(tsv=None):
    if tsv:
        return sort_entries(collect_terms(load_tsv(tsv, INPUT_DIR)))
    return sort_entries(collect_terms(load_tsv(TSV_NAME, INPUT_DIR)))

#This method is used to collect the terms from the TSV file loaded in memory
#It receives in input a list having a document per entry.
#The output of this method is to be consumed by those in charge of building the posting lists
#The method build an ordered list of terms:
#We read here all the documents one at a time.
#For each term read it writes the term itself along with the observed
#occurrence in the current document. 
def collect_terms(list_of_lists):
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
        		#The code TTT is used to delimit words in the title
            if t == 'TTT':
                title = not title
            #The code III is used to delimit words in the title
            elif t == 'III':
                ing = not ing
            #Creates an Entry with the information obtained
            else:
                if title:
                    entry = ParsedEntry(t, doc_id, -doc_pos)
                elif ing:
                    entry = ParsedEntry(t, doc_id, INGR_NEG_OFFSET - doc_pos)
                else:
                    entry = ParsedEntry(t, doc_id, doc_pos)
					 
					 #Add the term to the structure and advance
                terms.append(entry)
                doc_pos += 1
        #Assign a new key to the next document
        doc_id += 1

    doc_number = doc_id + 1
    print 'Terms collected...'
    return terms

#This method is used to build the posting lists
#It received as input all the words appearing in the corpus in alphabetic order;
#for each repetition of each word, the document and the corresponding position are also specified.
def sort_entries(list_pe):
    print 'Building index...'
    parsed_entries = sorted(list_pe, key=lambda parsed_entry: parsed_entry.term)
    num_entries = len(parsed_entries)

    dictionary = {}
    index = 0
    #For each term read from the ordered list of words received
    while index < num_entries:
        current_term = parsed_entries[index].get_term()
        term_dictionary = []
        print 'term {} of {}'.format(index, num_entries)
		  
		  #Until the term read is the same
        while index < num_entries and parsed_entries[index].get_term() == current_term:
            current_doc_id = parsed_entries[index].get_doc_id()
            position_list = []
            title = 0
            ing = 0
            occurs = 1
            
            #For each occurrence of the current term in the same document
            while index < num_entries and\
                    parsed_entries[index].get_term() == current_term and\
                    parsed_entries[index].get_doc_id() == current_doc_id:
					 
					 #VEDI UN PO' SE TOGLIERLO
                # To cumulate weight of repeated words
                pos = parsed_entries[index].get_doc_position()
                #According to our structures: 
                #all the positions < -1000 are reserved for ingredients
                if pos <= -1000:
                    ing += 1/occurs
                    parsed_entries[index].set_doc_position(-(pos + 1000))
                #all the positions -1000< x < 0 are reserved for the words in the title
                elif pos <= 0:   #L'UGUALE È UN ERRORE IN QUANTO IL TITOLO NON È MAI IN POSIZIONE 0
                    title += 1/occurs
                    parsed_entries[index].set_doc_position(-pos)
					 
					 #Store all the positions of the occurrences of the term in the document
                position_list.append(parsed_entries[index].get_doc_position())
					 
					 #Read new line
                index += 1
                #Increments occurrences counter
                occurs += 1
                
			   #Compute the term frequency in the current document weighting differently different parts of the document
            tf_td = math.log10(1.0 + len(position_list) + title*TITLE_WEIGHT + ing*ING_WEIGHT)
           	
           	#Create an object containing the tf score and the occurrences of the term in the document
            term_doc_entry = LabeledList(current_doc_id, position_list, tf_td)
            #Append the object to the current posting list
            term_dictionary.append(term_doc_entry)
            
        #Compute the inverse document frequency
        idf = math.log10((float(doc_number) / len(term_dictionary)))
        #Create and insert in the dictionary the posting list of "current_term" with the corresponding documents and idf.
        entry_dict = LabeledList(current_term, term_dictionary, idf)
        dictionary[current_term] = entry_dict

    print 'Index built'
    return dictionary

if __name__ == '__main__':
    from utils.utility_functions import ensure_dir

    ensure_dir(INPUT_DIR)
    ensure_dir(OUTPUT_DIR)
    build_index_json()
