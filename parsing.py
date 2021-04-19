import re
import os
import zipfile


# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)

# define punctuation
punctuations = '''!()-[]{};:'"\,\`<>./?@#$%^&*_~'''
stopwords_set = set()

#where we'll store all our words from the text
word_dic = {}

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
    
for file in allfiles:
    with open(file, 'r', encoding='ISO-8859-1') as f:
        filedata = f.read()
        result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents

        x = 1
        #for every document-- get the doc# and the doc#'s text
        for document in result[0:1]:
            # Retrieve contents of DOCNO tag
            docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            # Retrieve contents of TEXT tag
            text = "".join(re.findall(text_regex, document))\
                      .replace("<TEXT>", "").replace("</TEXT>", "")\
                      .replace("\n", " ")
            
            # step 1 - lower-case words, remove punctuation, remove stop-words, etc. 
            text = text.lower() # lower-case words

            word = ""
            for char in text:
                if char in punctuations: # remove punctuation
                    text = text.replace(char,'')
                elif char.isspace() == False:
                    word+=char
                elif char.isspace() == True:
                    if word in stopwords_set:
                        text=text.replace(' ' + word + ' ', ' ')  # Removes stopwords
                        word=""
                    #input into our token dictionary
                    if word not in word_dic:
                        word_dic[word] = 1
                        word=""
                    else:
                        word_dic[word]+=1
                        word=""
 
            print("Doc#: "+docno)
            print("Text: "+text)

            if 'has' in word_dic:
                print("value of has = "+ str(word_dic['has']))
            
            
            

            # step 2 - create tokens 
            
            # step 3 - build index
            