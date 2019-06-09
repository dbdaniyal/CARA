import csv
import os
import pickle
import string
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from math import *
from decimal import Decimal
from scipy import spatial, sqrt
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import gc

LOG = False

########################################################################
############### Functions ##########################################
########################################################################

#TF-IDF on reference papers
def tfIdfOfRefrencePapers(referenceSentence):

    global tfidf_transformer_Ref
    global countVectorOfRef
    tf_idf_vector_doc = tfidf_transformer_Ref.transform(countVectorOfRef.transform([referenceSentence]))
    # the following code stores the vectors value in queryVector and documentVector
    var = 0
    documentVector = []
    feature_names = countVectorOfRef.get_feature_names()
    # print(feature_names)
    # print matching column of query tokens from corpus token and print the value
    for col in tf_idf_vector_doc.nonzero()[1]:
        #print(feature_names[col], ' - ', tf_idf_vector_doc[0, col])
        documentVector.insert(var, round(tf_idf_vector_doc[0, col],3))
        var += 1
    return documentVector

#TF-IDF on query sentence
def tfIdfOfQuerySentence(querySentence):
    #global tfIdfCitation  # train data of cited paper
    global countVectorOfRef
    global tfidf_transformer_Ref
    tf_idf_vector_query = tfidf_transformer_Ref.transform(countVectorOfRef.transform([querySentence]))
    #response = tfIdfCitation.transform([querySentence])
    var = 0
    queryVector = []
    feature_names = countVectorOfRef.get_feature_names()
    #feature_names = tfIdfCitation.get_feature_names()
    # print(feature_names)
    for col in tf_idf_vector_query.nonzero()[1]:
        #print(feature_names[col], ' - ', round(tf_idf_vector_query[0, col],3))
        queryVector.insert(var, round(tf_idf_vector_query[0, col],3))
        var += 1
    return queryVector
#To tokenize
def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = []
    for item in tokens: #stem
        stems.append(nltk.PorterStemmer().stem(item))
    return stems
    #return tokens

#Eucledian distance
def euclidean_distance(x, y):
    return sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))

#Manhattan distance
def manhattan_distance(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))

#Minkowski distance
def nth_root(value, n_root):
    root_value = 1 / float(n_root)
    return round(Decimal(value) ** Decimal(root_value), 3)
def minkowski_distance(x, y, p_value):
    return nth_root(sum(pow(abs(a - b), p_value) for a, b in zip(x, y)), p_value)

#Jaccard similarity
def jaccard_similarity(x, y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    if(union_cardinality == 0):
        print("divide by zero")
        return 1

    return intersection_cardinality / float(union_cardinality)

################# Cosine similarity #####################
def square_rooted(x):
    return round(sqrt(sum([a * a for a in x])), 3)

def cosine_similarity(x, y):
    numerator = sum(a * b for a, b in zip(x, y))
    denominator = square_rooted(x) * square_rooted(y)
    if(denominator == 0):
        denominator = 1
    return round(numerator / float(denominator), 3)
############################################################
#Print Similarity Results
def cleanData(rawText):
    b = "_+=)(*[]{}&^%$#@!~`?/>.<,|\:;\"\'"
    rawText = rawText.replace("b\'", "")
    for char in b:
        rawText = rawText.replace(char, '')
    return rawText
def print_similarity_results(queryVector, documentVector):
    temp = []
    cosineScore = str(cosine_similarity(queryVector, documentVector))
    eucledianScore = (1 - euclidean_distance(queryVector, documentVector))
    manhattanScore = (1-manhattan_distance(queryVector, documentVector))
    minkowskiScore = (1 - minkowski_distance(queryVector, documentVector, 3))
    jaccardScore = (jaccard_similarity(queryVector, documentVector))
    temp.insert(0,cosineScore)
    temp.insert(1,eucledianScore)
    temp.insert(2,manhattanScore)
    temp.insert(3,minkowskiScore)
    temp.insert(4,jaccardScore)
    # print("C : " + str(cosineScore))
    # print("E : " + str(eucledianScore))
    # print("Man : " + str(manhattanScore))
    # print("Mink : " + str(minkowskiScore))
    # print("J : " + str(jaccardScore))
    return temp
#def print_similarity_results(queryVector, documentVector):
  #  temp = str(cosine_similarity(queryVector, documentVector))
 #   return temp
# Finding the similarity and return the sentence , similarity score , sentence length and document length
def query_doc_similarity(sentenceKey ,documentVector , citanceNumber):
    temp = []
    queryVector = []
    j=0
    temp.insert(j,Dict[citanceNumber].get(sentenceKey))
    citingSentence = temp[0]
    #print(citingSentence)

    citingSentence = cleanData(citingSentence)
    queryVector = tfIdfOfQuerySentence(str(citingSentence))

    if(LOG == False):
        temp = print_similarity_results(queryVector, documentVector)
        #temp1 = [citingSentence,temp,len(queryVector)]
        return temp


def combineSimilarity(sentence , documentVector):

    sentence = cleanData(sentence)
    queryVector = tfIdfOfQuerySentence(str(sentence))
    if (LOG == False):
        temp = print_similarity_results(queryVector, documentVector)
        # temp1 = [citingSentence,temp,len(queryVector)]
        return temp


file = open("DataForSimilarity.csv", 'r', encoding="utf-8")
reader = csv.reader(file)
Dict = []
tt=0

for line in reader:
    if(tt > 0):  # bcz in row 0 headings are written (citationSntence, refrenceArticle, ...)
        #print(line[0])
        #print(tt)
        Dict.insert(tt, {'citanceNumber': line[0], 'referenceArticle': line[1], 'citingArticle': line[2],'preTwo':line[3], 'preOne':line[4], 'citationSentence':line[5],
                         'postOne':line[6], 'postTwo':line[7]})

    tt+=1
#path = "C:/Users/dsumedialab/Desktop/CARA/CS-412 FYP/Data/Training-Set-2018"
path = "E:/DSU Semesters/8th Semester/CS-412 FYP/Data/Training-Set-2018"
#path="C:/Users/mh120/Desktop/Semester 8/CS-Project 2/scisumm-corpus/data/Training-Set-2018"
#path = "C:/Users/mh120/Desktop/Semester 8/CS-Project 2/scisumm-corpus/data/Training-Set-2019/Task1/From-Training-Set-2018"
path=os.path.realpath(path)
directoryList = os.listdir(path)
tempFoldername = ""
tempCitingFileName = ""
refPaperSentences = []
citingPaperText = []

tableCounter=0
tableDataCosine = []
tableDataEucledian = []
tableDataManhattan = []
tableDataMinkowski = []
tableDataJaccard = []

resultsCosine = []
resultsEucledianScore = []
resultsManhattanScore = []
resultsMinkowskiScore = []
resultsJaccardScore = []


###########################################
###### Main Logic Code ####################
###########################################
i = 401
while i< len(Dict):
    fname = Dict[i].get("referenceArticle")
    folderName = fname.split(".xml")  # In CSV the file name is written i.e C00-2123.xml after splitting C00-2123
    citingFileName = Dict[i].get("citingArticle")
    if(tempFoldername != folderName[0]):
        tempPath = os.path.join(path, folderName[0] + "\\Reference_XML")  # path of the refrence paper
        fnamePath = os.path.join(tempPath, fname)
        ###############################
        ####### XML Parsing ##########
        ###############################
        try:
            tree = ET.parse(fnamePath)
            root = tree.getroot()
            k = 0
            for child in root:
                for data in root.iter('S'):
                    Sid = data.get('sid')
                    yy = data.text.encode('UTF-8')
                    refPaperSentences.insert(k, yy)
                    k += 1
                break
            ################ Removing the special characters ###########################
            b = "_+=)(*[]{}&^%$#@!~`?/><,|\:;\"\'"
            refPaperSentencesString = str(refPaperSentences)
            refPaperSentencesString = refPaperSentencesString.replace("b\'", "")
            for char in b:
                refPaperSentencesString = refPaperSentencesString.replace(char, ' ')
            ##############################################################################
            countVectorOfRef = CountVectorizer(tokenizer=tokenize, max_df=0.85, stop_words='english', max_features=10000)
            word_count_vector = countVectorOfRef.fit_transform(str(refPaperSentencesString).split('.'))
            #print("TF :")
            #print(countVectorOfRef.vocabulary_)
            #print(list(countVectorOfRef.vocabulary_.keys()))
            tfidf_transformer_Ref = TfidfTransformer(smooth_idf=True, use_idf=True)
            tfidf_transformer_Ref.fit(word_count_vector)
            #print("IDF: ")
            #print(tfidf_transformer_Ref.idf_)
        except ParseError:
            print()
    ############## Compute The Similarity Scores ###############################################
    documentVector = tfIdfOfRefrencePapers(str(refPaperSentencesString))
    preTwoSimilarity = query_doc_similarity("preTwo", documentVector, i)
    preOneSimilarity = query_doc_similarity("preOne", documentVector, i)
    citationSentenceSimilarity = query_doc_similarity("citationSentence", documentVector, i)
    combineCitationAndPreOneSimilarity = combineSimilarity(Dict[i].get("preOne")
                                                           + Dict[i].get("citationSentence")
                                                           , documentVector)
    postOneSimilarity = query_doc_similarity("postOne", documentVector, i)
    postTwoSimilarity = query_doc_similarity("postTwo", documentVector, i)
    combineCitationAndPostOneSimilarity = combineSimilarity(Dict[i].get("citationSentence")
                                                           + Dict[i].get("postOne")
                                                           , documentVector)
    print("Iteration:" + str(i))
    resultsCosine = [i,preTwoSimilarity[0], preOneSimilarity[0], citationSentenceSimilarity[0],
               postOneSimilarity[0],postTwoSimilarity[0],combineCitationAndPreOneSimilarity[0]
        ,combineCitationAndPostOneSimilarity[0],citingFileName,fname,str(len(documentVector))]
    resultsEucledianScore = [i,preTwoSimilarity[1], preOneSimilarity[1], citationSentenceSimilarity[1],
               postOneSimilarity[1],postTwoSimilarity[1],combineCitationAndPreOneSimilarity[1]
        ,combineCitationAndPostOneSimilarity[1],citingFileName,fname,str(len(documentVector))]
    resultsManhattanScore = [i,preTwoSimilarity[2], preOneSimilarity[2], citationSentenceSimilarity[2],
               postOneSimilarity[2],postTwoSimilarity[2],combineCitationAndPreOneSimilarity[2]
        ,combineCitationAndPostOneSimilarity[2],citingFileName,fname,str(len(documentVector))]
    resultsMinkowskiScore = [i,preTwoSimilarity[3], preOneSimilarity[3], citationSentenceSimilarity[3],
               postOneSimilarity[3],postTwoSimilarity[3],combineCitationAndPreOneSimilarity[3]
        ,combineCitationAndPostOneSimilarity[3],citingFileName,fname,str(len(documentVector))]
    resultsJaccardScore = [i, preTwoSimilarity[4], preOneSimilarity[4], citationSentenceSimilarity[4],
                             postOneSimilarity[4], postTwoSimilarity[4], combineCitationAndPreOneSimilarity[4]
        ,combineCitationAndPostOneSimilarity[4], citingFileName, fname, str(len(documentVector))]

    tableDataCosine.insert(tableCounter, resultsCosine)
    tableDataEucledian.insert(tableCounter, resultsEucledianScore)
    tableDataManhattan.insert(tableCounter, resultsManhattanScore)
    tableDataMinkowski.insert(tableCounter, resultsMinkowskiScore)
    tableDataJaccard.insert(tableCounter, resultsJaccardScore)
    tableCounter+=1
    tempFoldername = folderName[0]  # for store the previous iteration reference paper name name
    tempCitingFileName = citingFileName  # for store the preevious cited paper name
    #################################################################################################


    if (i == (len(Dict)-1)):
        pickle.dump(tableDataCosine, open("pickleCosine_3.p", "wb"))
        pickle.dump(tableDataEucledian, open("pickleEucledian_3.p", "wb"))
        pickle.dump(tableDataManhattan, open("pickleManhattan_3.p", "wb"))
        pickle.dump(tableDataMinkowski, open("pickleMinkowski_3.p", "wb"))
        pickle.dump(tableDataJaccard, open("pickleJaccard_3.p", "wb"))
        tableCounter = 0
        break
    i += 1

#############################################################
###### Store Results to CSV #################################
#############################################################
""""
headers = ["CitanceNumber","PreTwo","PreOne","CitationSentence","PostOne","PostTwo"
    ,"PreOne And Citation" , "Citation And PostOne"
    ,"CitingArticle","ReferenceArticle","LengthOfDocumentVector"]
csvFile = open('Approach_501_664.csv', 'w', newline='')
#Use csv Writer
csvWriter = csv.writer(csvFile)
csvWriter.writerow(headers)
for eachRow in tempTableData:
    csvWriter.writerow([eachRow[0]+1, eachRow[1], eachRow[2],
                        eachRow[3],eachRow[4],eachRow[5],eachRow[6],eachRow[7],eachRow[8]
                           , eachRow[9], eachRow[10]])

##############################################################
"""