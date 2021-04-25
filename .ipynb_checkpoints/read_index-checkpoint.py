import os
import sys
import ast

# This file should contain code to receive either a document-id or 
# word or both and output the required metrics. See the assignment 
# description for more detail.


term_dictionary = {}
docno_dictionary = {}

def get_doc_info(file_name):
    global docno_dictionary
    filer = open(file_name, "r")
    contents = filer.read()
    docno_dictionary = ast.literal_eval(contents)
    filer.close()


def get_content(file_name):
    global term_dictionary
    # filer = open(file_name, "r")
    with open(file_name, 'r') as f:
        for line in f:
            print(line) 

def getInput(arguments):
    if len(arguments) <= 1 :
        return ""
    query_type = arguments[1]
    query = arguments[2]
    
    print("Query Type: "+str(query_type))
    print("Query: "+str(query))

    if query_type == "--term":
        term_attr = get_term_attributes(query)
        if len(term_attr) != 0:
            print(str(term_attr))
    elif query_type == "--doc":
        doc_attr = get_doc_attributes(query)
        if len(doc_attr) != 0:
            display_doc_attr(query, doc_attr)
    else:
        print("Error in Input")

def display_doc_attr(query, doc_attr):
    print("Listing for document:"+str(query))
    print("Total terms: "+str(doc_attr[0]))
    print("Distinct terms: "+str(doc_attr[1]))


def get_term_attributes(token):
    if token not in term_dictionary:
        return []
    else:
        return term_dictionary[token]

def get_doc_attributes(document):
    if document not in docno_dictionary:
        return []
    else:
        return docno_dictionary[document]


def main():
    
    print("in here..")
    get_content("text_file.txt")
    # print("loaded terms...")
    # get_doc_info("doc_file.txt")
    # print("loaded docs...")
    # print('Number of arguments:', len(sys.argv), 'arguments.')
    # print('Argument List:', str(sys.argv))
    # getInput(sys.argv)
    
if __name__ == "__main__":
    main()