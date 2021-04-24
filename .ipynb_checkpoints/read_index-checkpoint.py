import os
import sys
import ast

# This file should contain code to receive either a document-id or 
# word or both and output the required metrics. See the assignment 
# description for more detail.


term_dictionary = {}
docno_dictionary = {}

def get_doc_info(file_name):
    filer = open(file_name, "r")
    contents = filer.read()
    docno_dictionary = ast.literal_eval(contents)
    filer.close()


def get_content(file_name):
    filer = open(file_name, "r")
    contents = filer.read()
    term_dictionary = ast.literal_eval(contents)
    filer.close()
    print(term_dictionary)


def main():
    print("Hello World!")
    get_content("text_file.txt")
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))


if __name__ == "__main__":
    main()