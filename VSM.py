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

# tearm uniqu // list //
def uniquTerm(document):
    termsUn = []
    for key,val in document.items():
        for w in preproces2(val):
            if w not in termsUn:
                termsUn.append(w)
    return termsUn # // list //

#  calculate the frecuance of each term in each document 
def termDocumentVector(terms,dcument):
    tf = {}
    for term in terms:
        tf [term]=[]
        for val in dcument.values():
            if term in val:
                tf[term].append(1)
            else :
                tf[term].append(0)
    return tf
# calculate df(t)
def documentFrecuance(termDoc):
    dfVector = {}
    for term, presence_list in termDoc.items():
        dfVector[term] = sum(presence_list)
    return dfVector  

#calculat IDF(t)
def invartedDocumentFrecuance(df, n):
    idf = {}
    for term, df_count in df.items():
        if df_count > 0:
            idf[term] = np.log(n/df_count)
        else:
            idf[term] = 0.0
    return idf


# calculate TF_IDF
def tF_IDF(tf,idf,doc):
        lis = {}
        tf_idf={}
        for key,val in tf.items():
            lis[key]=[]
            for v in val:
                lis[key].append(idf[key]*v)
        docName = list(doc.keys())
        for i in docName:
            tf_idf[i]=[]
        for key,val in lis.items():
            for ind,v in enumerate(val):
                tf_idf[docName[ind]].append(v)    
        return tf_idf

            
    

# Represent the Query
def queryRepresent(doc_terms,query):
    queryVector = []
    for tDoc in doc_terms:
        if tDoc in query:
            queryVector.append(1)
        else:
            queryVector.append(0)
    return queryVector   

# dot prodect 
def dotProdect(queryV,docV):
    sumOf=0
    for index,val in enumerate(docV):
        sumOf+=(val*queryV[index])
    return sumOf
#magnitude of
def magnitudeOf(m):
    sumOf=0
    for dig in m:
        sumOf+=dig**2
    return np.sqrt(sumOf)    




# calculate cosaien simularity cos(Q,D)
def cosSimularity(query,docVec):
    qMagnitudeOf = magnitudeOf(query)
    cosDec={}
    for key,val in docVec.items():
        cosDec[key]=[]
        dotP=dotProdect(query,val)
        docMagnitudeOf = magnitudeOf(val) 
        cosDec[key].append(dotP/(qMagnitudeOf*docMagnitudeOf))
    return cosDec





# main
def vectorSpaceModel(query, dic):
    n=len(dic)
    terms= uniquTerm(dic)
    clean_doc=clteanDocument(dic)
    tDocVec=termDocumentVector(terms,clean_doc) # dic{'term':1,0,1}
    

    df=documentFrecuance(tDocVec) # how many term fre in the doc
    idf=invartedDocumentFrecuance(df,n)
    tf_idf=tF_IDF(tDocVec,idf,clean_doc)
    print(tF_IDF)
    #Preprocess Query 
    cleanQuery = preproces2(query)

    queryVec=queryRepresent(terms,' '.join(cleanQuery))
    
    # cosaien simularity 
    cos=cosSimularity(queryVec,tf_idf)
    # sorted result
    result = sorted(cos.items(), key=lambda item: item[1], reverse=True)
    print(result)
    finalResult = []
    for val in result:
        s = val[1]
        if s[0] != 0:
            text = dic.get(val[0], "ERROR")
            finalResult.append(val[0] + " " + text +" ("+ str(round(s[0],2))+")")
    return finalResult



