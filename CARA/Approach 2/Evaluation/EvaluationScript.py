import csv
import os
import pickle

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

path="E:/DSU Semesters/8th Semester/CS-412 FYP/Approach_2 Sentence to Sentence 2019/Improved Similarity For Approach 2 Using Lemm and Ignoring Citance/Updated Approach 2/PicklesFinalized"
path=os.path.realpath(path)
directoryList = os.listdir(path)

i = 0
pickleDataArr = []
pickleFileLoopCounter = 0

tempPickleCounter = 0
predictReferenceAnnotated = []
counterForPredictAnnotated = 0
rrr = 0
directoryList = sorted(directoryList)
#for a in directoryList:
 #   print(a)
for pickleFile in directoryList:
    print("Pickle Name : " + str(pickleFile))

    fnamePath = os.path.join(path, pickleFile)
    pickleDataArr = pickle.load(open(fnamePath,"rb"))
    k = 0
    Dict_Results = []  # contains all the entries of a csv file
    Dict_Results_counter = 0  # counter for above dictionary
    for line in pickleDataArr:
        Dict_Results.insert(Dict_Results_counter,
                                {'rowCount': line[0], 'citanceNumber': line[1], 'refFolderCount': line[2],
                                 'referenceArticle': line[3], 'citingArticle': line[4], 'CosineScore': line[5],
                                 'referencePaperSentence': line[10]})
        Dict_Results_counter += 1
    j = 0
    a = 0
    while a < len(Dict_Results):
        if(Dict_Results[a].get("citanceNumber") != Dict_Results[a+1].get("citanceNumber")):
            tempPickleCounter+=1
        if(a+1 == (len(Dict_Results)-1)):
            break
        a+=1
    #print("temp counter : " + str(tempPickleCounter))
    #pickleFileLoopCounter = pickleFileLoopCounter+200
    #print("temp  : "+str(tempPickleCounter))
    #print("len of pickleDataArr: "+str(len(pickleDataArr)))
    maxValArr = []
    maxValArrCount = 0

    referenceAnnotatedSentences = []
    counterForAnnotatedSentences = 0
    referenceAnnotatedOffset_temp = []
    # Loop to get referenceAnnotated Sentences

    evaluationScore = 0
    while i <= tempPickleCounter:
        print("i = "+str(i))
        referenceAnnotatedOffset = []
        refAnnCounter = 0
        referenceAnnotatedOffset = Dict_CARA[i].get('refAnnotatedOffsets')
        temp3 = referenceAnnotatedOffset.split(',')
        l = 0
        removalChars = " []\'"
        while (l != len(temp3)):
            for char in removalChars:
                temp3[l] = temp3[l].replace(char, '')
            referenceAnnotatedOffset_temp.insert(refAnnCounter, temp3[l])
            refAnnCounter += 1
            l += 1

        # citanceNumberTemp = Dict_Results[]
        citanceNumber = Dict_CARA[i].get('citanceNumber')
        citingArticle = Dict_CARA[i].get('citingArticle')
        referenceAricle = Dict_CARA[i].get('referenceArticle')
        abc = Dict_Results[k].get('citanceNumber')
        xyz = Dict_CARA[i].get('citanceNumber')
        #if(Dict_Results[k].get('citanceNumber')) == (Dict_CARA[i].get('citanceNumber')):
         #   print("inside IF $$$$$$$$$$$$$$$$$$$$$$4")
        #print(Dict_Results[k].get('citanceNumber'))
        #print(Dict_Results[k+1].get('citanceNumber'))
        #print(Dict_CARA[i].get('citanceNumber'))
        flag = False
        #print("k : "+str(k))
        #print("len dict_res : "+str(len(Dict_Results)))
        while ((Dict_Results[k].get('citanceNumber')) == (Dict_Results[k + 1].get('citanceNumber'))):
            #print(k)
            if (flag == True):
                maxValArr.insert(maxValArrCount,{"offset": Dict_Results[k + 1].get('rowCount'), "score": referenceAnnotatedScore})
                maxValArrCount += 1
                #k += 1
                break
            referenceAnnotatedScore = Dict_Results[k].get('CosineScore')
            # print(referenceAnnotatedScore)
            maxValArr.insert(maxValArrCount,{"offset": Dict_Results[k].get('rowCount'), "score": referenceAnnotatedScore})
            maxValArrCount += 1
            #if(k == len(pickleDataArr)-1):
             #   break
            k += 1

            if (k == (len(Dict_Results) - 1)):
                #print("inside")
                #print(k)
                #print(len(Dict_Results) - 1)
                k = k - 1
                flag = True
        maxValArr = sorted(maxValArr, key=lambda q: q['score'], reverse=True)

        maxValArr = maxValArr[0:5]
        k+=1
        m = 0
        predictedOffsetsOnly = ""
        #print("LENGTH : " + str(len(maxValArr)))
        if(len(maxValArr) ==5 ):
            while m < 5:
                predictedOffsetsOnly = predictedOffsetsOnly + str(maxValArr[m].get('offset') )+ " , "
                n = 0
                while n < len(referenceAnnotatedOffset_temp):
                    #print(referenceAnnotatedOffset_temp[n])
                    #print(maxValArr[m].get('offset'))
                    if (str(maxValArr[m].get('offset')) == referenceAnnotatedOffset_temp[n]):
                        print("Prdict & Actual Matched!!")
                        evaluationScore = (1 / len(referenceAnnotatedOffset_temp)) + evaluationScore
                        # break
                    n += 1
                m += 1
        #elif((len(maxValArr) == 0) and (len(referenceAnnotatedOffset_temp) == 1)):
         #   predictedOffsetsOnly = 0
          #  evaluationScore = 1

            predictReferenceAnnotated.insert(counterForPredictAnnotated, {
                'citanceNumber': citanceNumber,
                'annotatedOffset': referenceAnnotatedOffset_temp,
                'citingArticle': citingArticle,
                'referenceArticle': referenceAricle,
                'predictedOffset': predictedOffsetsOnly,
                'evaluationScore': evaluationScore
            })
        referenceAnnotatedOffset_temp = []
        counterForPredictAnnotated += 1
        evaluationScore = 0

        maxValArr = []
        maxValArrCount = 0
        i += 1

    #if(rrr == 1):
     #   break

    #print("rrr = " + str(rrr))
    #rrr+=1


csvFileObj = open('ResultsPredicted.csv', 'w', newline='')
csvWriter = csv.writer(csvFileObj)

# Headers of CARA csv file
csvWriter.writerow(["Citance Number" ,"Citing Article" , "Reference Article" ,"Annotated Offset","Predicted Offset", "Evaluation Score"])

i=0
while i < len(predictReferenceAnnotated):
    csvWriter.writerow(
        [predictReferenceAnnotated[i].get('citanceNumber')
            ,predictReferenceAnnotated[i].get('citingArticle')
            ,predictReferenceAnnotated[i].get('referenceArticle')
            ,predictReferenceAnnotated[i].get('annotatedOffset')
            ,predictReferenceAnnotated[i].get('predictedOffset')
            ,predictReferenceAnnotated[i].get('evaluationScore')
         ])
    i += 1
