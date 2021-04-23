import re
import os
import zipfile
# import string library function 
import string 
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

class term_attributes:
  
  def __init__(self, doc_id , list_of_pos, frequency):
    self.doc_id = doc_id
    self.list_of_pos = list_of_pos
    self.frequency = frequency

  def get_id(self):
      return self.doc_id
 
  def get_list_of_pos(self):
      return self.list_of_pos
  
  def get_frequency(self):
      return self.frequency

# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)

# define punctuation
stopwords_set = set()

#where we'll store all our words from the text
word_dic = {}
#where we'll store all our docno's and unique terms, total terms , etc.
docno_dic = {}

# inverted indices to map the ids
# tokenization process is as a conversion from a document to a sequence of (term_id, doc_id, position) 
# tuples which need to be stored in your inverted index.
termIndex = {}
docIndex = {}

with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
    zip_ref.extractall()

# putting the stopwords into a set data structure for easy comparison
with open('stopwords.txt') as f:
    lines = f.readlines()
    for word in lines:
        word = word.rstrip()
        stopwords_set.add(word)
   
# Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
    allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]
    
x = 1
print("Length of all files = "+str(len(allfiles)))

for file in allfiles:

    print("in file number = "+str(x))
    with open(file, 'r', encoding='ISO-8859-1') as f:
        filedata = f.read()
        result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents

         #for every document-- get the doc# and the doc#'s text
        print("There are  "+str(len(result))+" documents in this document")
        for document in result[0:1]:
            
            # Retrieve contents of DOCNO tag
            docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            
            # Retrieve contents of TEXT tag
            text = "".join(re.findall(text_regex, document))\
                      .replace("<TEXT>", "").replace("</TEXT>", "")\
                      .replace("\n", " ")

            #remove punctuation
            text = text.translate(str.maketrans('', '', string.punctuation))
            
            text = text.lower() 
            words = text.split() 

            local_dic = {}
            
            ps = PorterStemmer()
            for w in words:
                print(w, " : ", ps.stem(w))
                
            # but first lets define how many times a word occurs and at what position
            for i, word in enumerate(words,start=1):
                if word in local_dic:
                    frequency = local_dic[word][1] + 1
                    local_dic[word][0].append(i)
                    local_dic[word][1] = frequency

                else:
                    local_dic[word] = [[i],1]


            total_terms = 0
            
            for term in local_dic:
                # print(term, '->', local_dic[term])
                mytuple = (docno,local_dic[term])
                frequency_of_term = len(local_dic[term][0])
                total_terms = total_terms + frequency_of_term
                # print(mytuple)

                if term not in word_dic:
                    if term not in stopwords_set:
                        word_dic[term] = [mytuple]
                else:
                    word_dic[term].append(mytuple)
            
                
            print("Text: "+text)
            docno_dic[docno] = (total_terms,len(local_dic))
            print("Doc#: "+docno+" total terms: "+str(total_terms)+" unique terms: "+ str(len(local_dic))) 
            print("Length of word dic at the end = "+str(len(word_dic)))

            for t in word_dic:
                print(t,'->',word_dic[t])


            exit(0) #testing on one document for now
            #we can remove the exit after we are positive our implementation works
                    

            
    x = x +1 #increment what file we are on
    print("size of dic = "+str(len(word_dic)))


print(sorted(word_dic))


            
            # step 2 - create tokens 
            # step 3 - build index
            