import pandas as pd
import nltk
import re
import numpy as np
from nltk.corpus import stopwords
nltk.download('stopwords')
# read file
def read_documents_from_csv(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    return dict(zip(df[df.columns[0]], df[df.columns[1]]))

def preproces2(text):
    stopWords = set(stopwords.words('english'))
    text = re.sub(r"\.", "", text)
    text = text.lower()
    tokens = text.split()
    clean = []
    for t in tokens:
        if (t not in stopWords):
            clean.append(t)
    return clean
#clean document
def clteanDocument(document):
    dec = {}
    for key,val in document.items():
        clean = preproces2(val)
        clean = ' '.join(clean)
        dec[key]=clean
    return dec

# function length document and avg
def lengthDoc(doc): # {d1:2,d2:6}
    lenDoc = {}
    for key,val in doc.items():
        lenDoc[key]=[]
        lenDoc[key]=len(val.split())
    return lenDoc

def avgInLenTermOfDocument(lenDoc):# avg for all doc
    n = len(lenDoc)
    sumOf = 0
    for val in lenDoc.values():
        sumOf+=val
    return sumOf/n

#TF for Query
def tfQuery(query,doc): # if term appear in the doc 1 , else 0 : {term1:[1,1,0,0,0]}
    tf = {}
    query = set(query)
    for i in query:
        tf[i] =[]
    for key,val in doc.items():
        for q in query:
            if q in val:
                tf[q].append(1)
            else:
                tf[q].append(0)    
    return tf
# claculate numper term in the doc
def n_term(val):
    return sum(val)


# calculate IDF
def IDF(listValueTerm): # return IDF {'c': [1, 1, 1], 'd': [0, 1, 1]}, in val[1, 1, 1] = 3
    nTerm = n_term(listValueTerm)
    return np.log(((nOfDoc-nTerm+0.5)/(nTerm+0.5)))

# calculate frecuance term in doc
def numberTerm(term,docVal):# calculate frecuance term in doc team = 'c' , doc='c c c', nt=3
    words = docVal.split()
    return words.count(term)

# calculate TF_IDF
def TF_IDF(term,docVal,k1,b=0.75):
    f_Q_D = numberTerm(term,docVal)
    if f_Q_D==0: # 0/num... = 0
        return 0
    numOfTermInDoc = len(docVal.split()) 
    return (f_Q_D*(k1+1))/(f_Q_D+k1*(1-b+b*numOfTermInDoc/avg))


# calculate BM25
def BM25_for_all_doc_term(allQueryTerms,allDoc,k1,b):
    decBM25 = {}
    result =0.0
    for nameDoc,valDoc in allDoc.items():               # all doc and val
        for term,appearInTerm in allQueryTerms.items(): # all query quTF {'cat': [1, 1, 1], 'dog': [0, 1, 1]}
            idf = IDF(appearInTerm)                     # for term in the query
            tf_idf=TF_IDF(term,valDoc,k1,b)             # for term and doc
            result+=(idf*tf_idf)                        # sum all idf (q1) * tf_idf(q1,D1)
        decBM25[nameDoc]=[]    
        decBM25[nameDoc]=result # decBM25[d1]= 0.78
        result = 0 # for next doc
    return decBM25





#                        // main //

def BM25(query, dic,k1,b=0.75):
    # preprocess document
    cleanDoc = clteanDocument(dic)
    global nOfDoc 
    nOfDoc= len(cleanDoc)
    lenTermInDocuments=lengthDoc(cleanDoc)
    global avg
    avg=avgInLenTermOfDocument(lenTermInDocuments)
    queryPreprocess=preproces2(query)
    quTF=tfQuery(queryPreprocess,cleanDoc)
    print("quTF" , quTF)
    print("cleanDoc" , cleanDoc)
    model=BM25_for_all_doc_term(quTF,cleanDoc,k1,b)
    result = sorted(model.items(), key=lambda item: abs(item[1]), reverse=True)
    finalResult = []
    for val in result:
        if val[1] != 0.0:
            text = dic.get(val[0], "ERROR")
            finalResult.append(val[0] + " " + text +": (" + str(round(val[1],2)) + ")")
    return finalResult



