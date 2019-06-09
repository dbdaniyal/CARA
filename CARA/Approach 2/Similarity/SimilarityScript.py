import csv
import os
import pickle
import xml.etree.ElementTree as ET
from datetime import time
from decimal import Decimal
from math import sqrt
from xml.etree.ElementTree import ParseError
import nltk
import gc
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import regex as re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

LOG = False

def citanceCategoryFunc(citance):
    strCitanceCategory = ""
    pA = r'(\([A-Za-z\, ]+ [0-9]{4}+\))'
    pB = r'(\([0-9]{4}\))'
    pC = r'(\([A-Za-z\, ]+[0-9]{4}[A-Za-z]{1}\))'
    pD = r'([A-Za-z]* \[[0-9]{1,4}\])'  # pB mdify hogi issay yey Arthur(2009) not only (2009)
    pE = r'(\[[0-9 \,]+\])'
    pF = r'(\([A-Za-z. \,]+[0-9]{4}+;?\)?)'
    pG = r'(\(?[A-Za-z \,]+[0-9]{4}+;?\)?)'  # Less errors
    pH = r'(\{[0-9]{4}\))'
    pI = r'(\([A-Za-z ]+ [0-9]{2}+\))'
    pJ = r'(\([0-9]{4}[A-Za-z]{1}\))'

    pAarr = re.findall(pA, str(citance))
    pBarr = re.findall(pB, str(citance))
    pCarr = re.findall(pC, str(citance))
    pDarr = re.findall(pD, str(citance))
    pEarr = re.findall(pE, str(citance))
    pFarr = re.findall(pF, str(citance))
    pGarr = re.findall(pG, str(citance))
    pHarr = re.findall(pH, str(citance))
    pIarr = re.findall(pI, str(citance))
    pJarr = re.findall(pJ, str(citance))

    pALength = len(pAarr)
    pBLength = len(pBarr)
    pCLength = len(pCarr)
    pDLength = len(pDarr)
    pELength = len(pEarr)
    pFLength = len(pFarr)
    pGLength = len(pGarr)
    pHLength = len(pHarr)
    pILength = len(pIarr)
    pJLength = len(pJarr)
    tempMax = (max(pALength, pBLength, pCLength, pDLength, pELength,
                   pFLength, pGLength, pHLength, pILength, pJLength))

    #print(citance)
    if (tempMax == 1): #single
      #  print("1")
        return 1
    elif (tempMax > 1): #multi
       # print("2")
        return 2
    else: # no citation marker found
        #print("0")
        return 0


#To tokenize
def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = []
    lemmatizer = WordNetLemmatizer()

    for item in tokens: #stem
        stems.append(nltk.PorterStemmer().stem(item))
        #stems.append(lemmatizer.lemmatize(item))
    return stems

#TF-IDF on reference papers
def tfIdfOfRefrencePapers(referenceSentence):
    global tfidf_transformer_Ref
    global countVectorOfRef
    tf_idf_vector_doc = tfidf_transformer_Ref.transform(countVectorOfRef.transform([referenceSentence]))
    #global tfidfRef
    #response = tfidfRef.transform([referenceSentence])
    # the following code stores the vectors value in queryVector and documentVector
    var = 0
    documentVector = []
    # print(feature_names)
    # print matching column of query tokens from corpus token and print the value
    for col in tf_idf_vector_doc.nonzero()[1]:
        #print(feature_names[col], ' - ', tf_idf_vector_doc[0, col])
        documentVector.insert(var, round(tf_idf_vector_doc[0, col],3))
        var += 1
    return documentVector

#TF-IDF on query sentence
def tfIdfOfQuerySentence(querySentence):
    global countVectorOfRef   # contain term document matrix
    global tfidf_transformer_Ref    # contain idf
    tf_idf_vector_query = tfidf_transformer_Ref.transform(countVectorOfRef.transform([querySentence]))
    #global tfIdfCitation  # trained tf-idf of citing paper
    #response = tfIdfCitation.transform([querySentence])
    var = 0
    queryVector = []
    # print(feature_names)
    # print matching column of query tokens from corpus token and print the value
    for col in tf_idf_vector_query.nonzero()[1]:
        #print(feature_names[col], ' - ', round(tf_idf_vector_query[0, col],3))
        queryVector.insert(var, round(tf_idf_vector_query[0, col],3))
        var += 1
    return queryVector

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
#Print Similarity Results and return sentence , similarity score , query length and document length
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
# Finding the similarity and return the sentence , similarity score , sentence length and document length
def query_doc_similarity(sentenceKey ,documentVector , citanceNumber):
    temp = []
    queryVector = []
    j=0
    temp.insert(j,Dict_CARA[citanceNumber].get(sentenceKey))
    #tempCitanceNum = Dict_CARA[0].get()
    citingSentence = temp[0]

    b = "_+=)(*[]{}&^%$#@!~`?/>.<,|\:;\"\'"
    citingSentence = citingSentence.replace("b\'", "")
    for char in b:
        citingSentence = citingSentence.replace(char, '')
    tempCitingArticle = Dict_CARA[citanceNumber].get('citingArticle')
    tempReferenceArticle = Dict_CARA[citanceNumber].get('referenceArticle')
    queryVector = tfIdfOfQuerySentence(str(citingSentence))
    if(LOG == False):
        temp = print_similarity_results(queryVector, documentVector)
        temp = [temp[0],temp[1],temp[2],temp[3],temp[4],tempCitingArticle]
        return temp

file = open("DataForSimilarity.csv", 'r')
reader = csv.reader(file)

Dict_CARA = [] #contains all the entries of a csv file
Dict_CARA_counter=0 #counter for above dictionary
for line in reader:
    if(Dict_CARA_counter > 0):  # bcz in row 0 headings are written (citationSntence, refrenceArticle, ...)
        Dict_CARA.insert(Dict_CARA_counter, {'rowCount':line[0],'citanceNumber': line[1], 'mainFolderCount': line[2],
                'referenceArticle': line[3],'citingArticle': line[4],
                'refAnnotatedOffsets':line[5],'citationSentence':line[6], 'citingPaperAuthors':line[7]})
    Dict_CARA_counter+=1
path="E:/DSU Semesters/8th Semester/CS-412 FYP/Data/Training-Set-2019/Task1/From-ScisummNet-2019"
#path="C:/From-ScisummNet-2019"
#path = "C:/Users/mh120/Desktop/Semester 8/CS-Project 2/scisumm-corpus/data/Training-Set-2019/Task1/From-ScisummNet-2019"

path=os.path.realpath(path)
directoryList = os.listdir(path)
rowCount = 0
tempFoldername = ""
tempCitingFileName = ""
refPaperSentences = []
citingPaperText = []
counter=0
result = []
tableData = []
pairOfRefAndCit = []
refFolderCount = 0
tempCitanceNum = 0

###########################################
############ Main Logic Code ##############
###########################################


tempRefPaperSentences = []
i=4499
while i< len(Dict_CARA):
    print("Iteration count : " + str(i))
    fname = Dict_CARA[i].get("referenceArticle")
    #preTwo = Dict[i].get("preTwo")
    #print(preTwo)
    folderName = fname.split(".xml")

    if(tempFoldername != folderName[0]):
        print("inside if")
        refPaperSentences = []
        tempRefPaperSentences = []
        k = 0
        tempPath = os.path.join(path, folderName[0] + "\\Reference_XML")
        fnamePath = os.path.join(tempPath, fname)
        #################################################
        ####### XML Parsing Of Reference Paper ##########
        #################################################
        try:
            tree = ET.parse(fnamePath)
            root = tree.getroot()
            for child in root:
                for data in root.iter('S'):
                    Sid = data.get('sid')
                    yy = data.text.encode('UTF-8')
                    yy = str(yy)
                    yy = yy.replace("b\'", "")
                    refPaperSentences.insert(k, yy)
                    tempRefPaperSentences.insert(k,yy)
                    k += 1
                break
            ############# Removing the special characters #####################
            b = "_+=)(*[]{}&^%$#@!~`?/><,|\:;\"\'"
            #refPaperSentencesString = str(refPaperSentences)
#            tempRefPaperSentences = refPaperSentences
            m = 0
            for a in refPaperSentences:
                a = str(a)
                for char in b:
                    a = a.replace(char, ' ')
                refPaperSentences[m] = a
                m+=1

            #refPaperSentencesString = refPaperSentencesString.replace("b\'", "")
            ####################################################################
            print(len(tempRefPaperSentences))
            if(len(refPaperSentences) > 1):
                countVectorOfRef = CountVectorizer(tokenizer=tokenize, max_df=0.85, stop_words='english',max_features=10000)
                word_count_vector = countVectorOfRef.fit_transform(refPaperSentences)
                # print("TF :")
                # print(countVectorOfRef.vocabulary_)
                # print(list(countVectorOfRef.vocabulary_.keys()))
                tfidf_transformer_Ref = TfidfTransformer(smooth_idf=True, use_idf=True)
                tfidf_transformer_Ref.fit(word_count_vector)
            # print("IDF: ")
            # print(tfidf_transformer_Ref.idf_)
            #tfidfRef = TfidfVectorizer(tokenizer=tokenize,stop_words='english')  # initialize object to tokenize the dictionary and remove stop words
            #tfsRef = tfidfRef.fit_transform(str(refPaperSentencesString).split('.')) # apply TF-Idf on reference paper
        except ParseError:
            print()
    #pairOfRefAndCit = [folderName[0], citingFileName]
    ############# Compute similarity with every sentence of reference paper ##################
    #if (pairOfRefAndCit[0] == tempFoldername and pairOfRefAndCit[1] != tempCitingFileName):
    """
    print(str(i))
    print(citingFileName)
    print(tempCitingFileName)
    print(tempFoldername)
    print(folderName[0])
    """
    j = i+1
    if (Dict_CARA[j].get("referenceArticle") == Dict_CARA[j - 1].get("referenceArticle")):
        tempCitanceNum += 1
        flag = tempCitanceNum
    else:
        flag = tempCitanceNum + 1
        tempCitanceNum = 0
        print("**************else")

    for refSentence in tempRefPaperSentences:
        #################### Compute Similarity ############################
        if (citanceCategoryFunc(refSentence) == 0):
            specialChars = "_+=)(*[]{}&^%$#@!~`?/><,|\:;\"\'"
            # refPaperSentencesString = str(refPaperSentences)
            for char in specialChars:
                refSentence = refSentence.replace(char, ' ')
            documentVector = tfIdfOfRefrencePapers(refSentence)
            citationSentenceSimilarity = query_doc_similarity("citationSentence", documentVector, i)

            results = [rowCount, flag, Dict_CARA[i].get("mainFolderCount"), fname, citationSentenceSimilarity[5],citationSentenceSimilarity[0]
                , citationSentenceSimilarity[1],citationSentenceSimilarity[2],citationSentenceSimilarity[3],citationSentenceSimilarity[4],refSentence]

            tableData.insert(counter,results)
            counter += 1
            rowCount += 1
    tempFoldername = folderName[0]  # for checking the previous iteration folder name
    ###########################################################################################
    rowCount = 0
    if(i == 4600):
        print("PICKLELING")
        pickle.dump(tableData, open("pickle_a"+str(i)+".p", "wb"))
        #tableData = []
        #counter = 0
        break
        # outer = os.getcwd()
        # cache = os.path.join(outer, 'cache')
        # for f in os.listdir(cache):
        #     f = os.path.join(cache, f)
        #     use_by = time.time() - 30 * 60
        #     if os.path.getatime(f) < use_by:
        #         os.remove(f)
    gc.collect()
    i+=1


#save
#pickle.dump(tableData,open("tableData.p","wb"))
#for i in tableData:
 #   print(i)
#print(tableData)

#tempTableData = []
#load
#tempTableData = pickle.load(open("pickleTwoHundred.p","rb"))

#############################################################
###### Store Results to CSV #################################
#############################################################

# headers = ["RowCount","CitanceNumber","RefFolderCount","RefrenceArticle","CitingArticle","CosineScore",
#            "EucledianScore","ManhattanScore","MinkowskiScore","JaccardScore","ReferencePaperSentence"]
# csvFile = open('Approach2_results_1-100.csv', 'w', newline='')
# #Use csv Writer
# csvWriter = csv.writer(csvFile)
# csvWriter.writerow(headers)
# for eachRow in tempTableData:
#     csvWriter.writerow([eachRow[0], eachRow[1], eachRow[2],eachRow[3],eachRow[4],eachRow[5],eachRow[6],
#                        eachRow[7], eachRow[8], eachRow[9], eachRow[10]])

##############################################################