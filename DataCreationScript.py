#In this code we changes some things on 5/4/2019
#in if condition we changes the , to 'or'

import csv
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import regex as re

path="E:/DSU Semesters/8th Semester/CS-412 FYP/Data/Training-Set-2018"
#path="C:/Users/mh120/Desktop/Data/scisumm-corpus/data/Training-Set-2018"

path=os.path.realpath(path)
#print(path + "***")
#print(os.listdir(path))
directoryList = os.listdir(path)
#print(directoryList)
#os.startfile(path)

csvFile = open('TEMP.csv', 'w', newline='')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["citanceNumber","referenceArticle","citingArticle","preTwo","preOne","citationSentence",
                    "postOne","postTwo","citationCategory"])

tempPre1Sentece = ""   #made this while workign with contiguous
tempPreSentences = []    #made this while workign with contiguous
tempPreSentencesCount = 0
categoryCounterForContiguous = 0
citanceCategory = ""
correctCount = 0
errorCount = 0
totalCount = 0
tempCitanceNumber=0

preCitanceId = 0 #make this while editing the case of contiguous sentence

aaa = 0
for folder in directoryList:
    tempPath = os.path.join(path, folder+"\\annotation")
    tempList = os.listdir(tempPath)
    fname = os.path.join(tempPath,tempList[0])
    print("Folder: " + folder)
    #print(fname)
    with open(fname, encoding="utf8") as annotatedData:
        #text = annotatedData.read()
        annotatedList = annotatedData.readlines()
        annotatedModifiedArray = []  # contains final modified and cleaned from of each annotation
        count = 0

        for word in annotatedList:
            if (word != '\n'):  # to remove line breaks in from overall data(all lines)
                word = word.replace('\n', '')  # to remove line breaks within a data (line)
                annotatedModifiedArray.insert(count, word)
                count += 1

        # for w in annotatedModifiedArray:   #to print modified array
        # print(w)

        iterator = 0  # loop iterator
        dataDict = []
        citanceNumber = 0
        referenceArticle = ""
        citingArticle = ""
        sID = []  # sentence ID (unique for each sentence in paper)
        # ssid = section sentence ID (unique onlye for each section, after the section it renews)
        sIDCount = 0

        while iterator < len(annotatedModifiedArray):
            mainStr = annotatedModifiedArray[iterator]
            splittedArr = mainStr.split('|')
            #print(splittedArr)
            # lstrip() function strips only leading space so the output will be:
            # ‘    This is Test String to strip leading space’
            # ‘This is Test String to strip leading space’"""

            # for citance number
            temp1 = splittedArr[0].split(':')
            citanceNumber = temp1[1].lstrip()
            # print(citanceNumber)

            # for reference article
            temp1 = splittedArr[1].split(':')
            referenceArticle = temp1[1]
            referenceArticle = temp1[1].lstrip()
            # print(referenceArticle)

            # for reference article
            temp1 = splittedArr[2].split(':')
            citingArticle = temp1[1]
            citingArticle = temp1[1].lstrip()
            # print(citingArticle)

            # for citation marker offset (tells the offset of citance only)
            temp1 = splittedArr[3].split(':')
            citanceMarkerOffset = temp1[1]
            removalChars = " []\'"
            for char in removalChars:
                citanceMarkerOffset = citanceMarkerOffset.replace(char, '')
            #print(citanceMarkerOffset)

            # print(citingArticle)

            # for citation text (sid)

            # 1- Getting offsets through citation offset
            temp1 = splittedArr[5].split(':')
            tempA = temp1[1].lstrip()
            temp2 = tempA.split(',')

            i = 0
            removalChars = " []\'"
            while (i != len(temp2)):
                for char in removalChars:
                    temp2[i] = temp2[i].replace(char, '')
                sID.insert(sIDCount, temp2[i])
                sIDCount += 1
                i += 1

            # 2- Getting offsets through citation text
            """temp1= splittedArr[6].split(':')
            temp2 = temp1[1]
            #print(temp2)
            temp3 = temp2.split('sid')
            #print(temp3)

            # = aae then space then 2/3 digits
            i = 1
            removalChars = "=\""
            while(i != len(temp3)):
                temp4 = temp3[i].split(' ')
                #print(temp4)
                temp5 = temp4[1]
                for char in removalChars:
                    temp5 = temp5.replace(char, '')

                sID.insert(sIDCount,temp5)
                sIDCount+=1
                i+=2
            """

            dataDict.insert(iterator, {'citanceNumber': citanceNumber,
                                       'referenceArticle': referenceArticle,
                                       'citingArticle': citingArticle,
                                       'sid': sID,
                                       'citanceMarkerOffset' : citanceMarkerOffset})
            iterator += 1
            citanceNumber = 0
            citingArticle = ""
            referenceArticle = ""
            sIDCount = 0
            sID = []
        postSentenceList = []
        preSentenceList = []

        for i in dataDict:
            #print(str(i))

            #tempCitanceNumber+=1
            #print("Citance of: " + folder)
            citingPaper = i.get('citingArticle')
            refrencePaper = i.get('referenceArticle')
            #print("citing article:-" + citingPaper)
            if(citingPaper.__contains__(".txt ")):
            #path = '.\C00-2123\Citance_XML\\' + str(citingPaper)
                spitter = citingPaper.split('.')
                citingPaper = spitter[0]
                citingPaper = citingPaper+'.xml'
            elif(citingPaper.__contains__(".xml ")):
                spitter = citingPaper.split('.')
                citingPaper = spitter[0]
                citingPaper = citingPaper + '.xml'
            else:
                spitter = citingPaper.split(' ')
                citingPaper = spitter[0]+'.xml'

            # for refrence Article naming cases
            if (refrencePaper.__contains__(".txt ")):
                # path = '.\C00-2123\Citance_XML\\' + str(citingPaper)
                spitter = refrencePaper.split('.')
                refrencePaper = spitter[0]
                refrencePaper = refrencePaper + '.xml'
            elif (refrencePaper.__contains__(".xml ")):
                spitter = refrencePaper.split('.')
                refrencePaper = spitter[0]
                refrencePaper = refrencePaper + '.xml'
            else:
                spitter = refrencePaper.split(' ')
                refrencePaper = spitter[0] + '.xml'
            #print("Citing Paper: " + citingPaper)
            a = i.get("sid")
            #print("Original SID : " + str(a[0]))
            try:
                citancePath = os.path.join(path,str(folder)+"\Citance_XML\\"+str(citingPaper))
                #print("Citance path:" + citancePath)
                # fname = os.path.join(path, 'C02-1050.csv')
                #print(path)
                # path = "E:\DSU Semesters\7th Semester\FYP 1\Implementation\Phase 2.1\C00-2123\C00-2123.xml"

                tree = ET.parse(citancePath)
                root = tree.getroot()
                #print("yes!" + citingPaper)

                a = i.get("sid")
                #print("After Tree: " + str(a[0]))

                matchingSid = i.get("sid")
                preSid = str(int(matchingSid[0]))
                tempListConti = []
                tempListContiCountr = 0
                #40,41
                #presid= 40
                #ciation marker = 40


                stopCondition = False
                postSid = int(matchingSid[len(matchingSid)-1])
                postSid += 1
                matchingSid1 = str(postSid)
                countPre = 0
                countPost = 0
                loopIter = len(matchingSid)
                for x in range(6):
                    for data in root.iter('S'):
                        Sid = data.get('sid')
                        #if(len(matchingSid) > 1):

                            #while i < len(matchingSid):
                             #   if()
                        if (Sid == preSid):
                            yy = data.text.encode('utf-8')
                            temp = len(matchingSid)

                            #print("*************************ksi : " + str(temp))
                            a = 1
                            if(stopCondition == False):
                                #print("bef sid : "+str(Sid))

                            #11 : They said tha we are ...
                            #12 : Once we were Starg(2011) etal.
                            #13 : burger(2011)jhdshoady /...


                                while a < temp:



                                    Sid = str(int(Sid) + 1)
                                    for tempData in root.iter('S'):
                                        if(Sid == tempData.get('sid')):
                                            #Sid = str(int(Sid)+1)
                                            #print("sid**&& : " + str(Sid))
                                            tempDecode= yy.decode('utf-8')

                                            """
                                            Contiguous cases:
                                                1- et.
                                                2- e.g.
                                                3- cf.
                                                4- al.
                                                5- et a!.
                                                6- et a!
                                            """

                                            if(tempDecode.endswith("et al.") or tempDecode.endswith("et.") or tempDecode.endswith("cf.") or tempDecode.endswith("al.") or tempDecode.endswith("et a!.") or tempDecode.endswith("et a!") or tempDecode.endswith("e.g.")):
                                                #print("**********catched!!!!")
                                                #print(citanceNumber)
                                                #print("Sentence : "+(str(tempData.text)))

                                                tempListConti.insert(tempListContiCountr,str(int(Sid)-1)) #40
                                                tempListContiCountr+=1
                                                tempListConti.insert(tempListContiCountr, str(Sid)) #41
                                                tempListContiCountr += 1

                                                yy = yy + tempData.text.encode('utf-8')
                                            else:
                                                #print("$$$$$Length : "+str(len(matchingSid)))
                                                #difference = (int(matchingSid[temp - 1]) - int(matchingSid[temp - 2]))
                                                #print("$$$$$DIFFERENCE : " + str(difference))

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
                                                #print("$$$SID : "+str(tempData.get('sid')))
                                                citanceId = tempData.get('sid')


                                                #checkCitance = len(re.findall(pA or pB or pC or pD or pE or pF or pG or pH or pI or pJ,str(tempData.text)))
                                                checkCitance = len(re.findall(pA, str(tempData.text)))
                                                checkCitance = len(re.findall(pB, str(tempData.text))) + checkCitance
                                                checkCitance = len(re.findall(pC, str(tempData.text))) + checkCitance
                                                checkCitance = len(re.findall(pD, str(tempData.text))) + checkCitance
                                                checkCitance = len(re.findall(pE, str(tempData.text))) + checkCitance
                                                checkCitance = len(re.findall(pF, str(tempData.text))) + checkCitance
                                                checkCitance = len(re.findall(pG, str(tempData.text))) + checkCitance
                                                checkCitance = len(re.findall(pH, str(tempData.text))) + checkCitance
                                                checkCitance = len(re.findall(pI, str(tempData.text))) + checkCitance
                                                checkCitance = len(re.findall(pJ, str(tempData.text))) + checkCitance
                                                #print("$$$Hello : "+str(checkCitance))

                                                #11 = if you say (Berger 20118) hello
                                                #12 = wonderful bhad ds

                                                #13 = wonderful bhad ds
                                                #14 = if you say (Berger 20118) hello

                                                if(checkCitance > 0):
                                                    categoryCounterForContiguous = tempCitanceNumber
                                                    checkCitance = 0
                                                    #tempPre1Sentece = yy
                                                    tempPreSentences.insert(tempPreSentencesCount,yy)
                                                    yy = tempData.text.encode('utf-8')
                                                    tempPreSentencesCount+=1
                                                    #break
                                                else:
                                                    tempPreSentences.insert(tempPreSentencesCount,
                                                                            tempData.text.encode('utf-8'))

                                    a += 1
                                    stopCondition = True
                            #print("Text : " + str(yy))
                            preSentenceList.insert(countPre, yy)
                            countPre += 1

                    preSid = int(preSid) - 1
                    preSid = str(preSid)

                for x in range(5):

                    for data in root.iter('S'):

                        if(int(preCitanceId) > 0):
                            matchingSid = str(preCitanceId)
                            preCitanceId = 0

                        Sid = data.get('sid')

                        # print(name)
                        if (Sid == matchingSid1):
                            # print("Saads SID : " + str(Sid))
                            yy = data.text.encode('utf-8')
                            # print("Text : " + yy)
                            postSentenceList.insert(countPost, yy)
                            countPost += 1

                    postSid += 1
                    matchingSid1 = str(postSid)

                #if(tempPre1Sentece != ""):
                 #   preSentenceList[1] = tempPre1Sentece
                lengthOfTempPreSentence = len(tempPreSentences) - 1
                if (len(tempPreSentences) > 0):
                    # print("in the ksi!!!!!!!!!!!!!!!!!!!!!" + str(len(tempPreSentences)))
                    c = 1
                    while lengthOfTempPreSentence >= 0:
                        if (tempPreSentences[lengthOfTempPreSentence].decode('utf-8').endswith("et al.") or
                            tempPreSentences[lengthOfTempPreSentence].decode('utf-8').endswith("ct al.") or
                            tempPreSentences[lengthOfTempPreSentence].decode('utf-8').endswith("et.") or
                            tempPreSentences[lengthOfTempPreSentence].decode('utf-8').endswith("cf.") or
                            tempPreSentences[lengthOfTempPreSentence].decode('utf-8').endswith("al.") or
                            tempPreSentences[lengthOfTempPreSentence].decode('utf-8').endswith("et a!.") or
                            tempPreSentences[lengthOfTempPreSentence].decode('utf-8').endswith("et a!") or
                            tempPreSentences[lengthOfTempPreSentence].decode('utf-8').endswith("e.g.") or
                            tempPreSentences[lengthOfTempPreSentence].decode('utf-8').endswith("(cf.")):
                            preSentenceList[c - 1] = tempPreSentences[lengthOfTempPreSentence] + preSentenceList[c - 1]
                        else:
                            preSentenceList[c] = tempPreSentences[lengthOfTempPreSentence]
                            c += 1
                        lengthOfTempPreSentence -= 1

                #print("Citance : " + str(preSentenceList[0]))
                #print("-1 : " + str(preSentenceList[1]))
                #print("+1 : " + str(postSentenceList[0]))

                #preSentences = ' '.join([str(elem) for elem in preSentenceList])
                #postSentences = ' '.join([str(elem) for elem in postSentenceList])
                #citationWindow = preSentences + postSentences
                # print(citationWindow)
                """
                Single Citance:                 main sentence that has a citation point
                Multi Citance:                  refers to a citing sentence that has multiple citation points within one sentence
                Contiguous-sentence citation:   refers to a multiple sentence citation with preceding or forgoing sentences(s) of citing sentence.
                Multi-sentence citation:        refers to citation text that may or may not be contiguous. 
                """


                #p1 = r'(.*\([A-Za-z]+ .* [0-9]{4}+\)\.+?)'          # p1 ... says that (Warren and Pereira, 1982).
                #p2 = r'(.*\([A-Za-z]+ .* [0-9]{4}+\)[^\.]+\.+?)'    # p2 ... says that (Warren and Pereira, 1982) but ... .
                #p8 = r'(.*\([A-Za-z\,]+ [0-9]{4}+\)\.+?)'  # p8 ... says that (Pereira, 1982).
                #p9 = r'(.*\([A-Za-z\,]+ [0-9]{4}+\)[^\.]+\.+?)'  # p9 ... says that (Pereira, 1982)....
                #for above cases:
                pA = r'(\([A-Za-z\, ]+ [0-9]{4}+\))'
                pAarr = []
                pALength = 0

                #p3 = r'(.*\([0-9]{4}\).*\.)'  # p3 ... that Waren and Pereira (2009) but .... .
                #for above case:
                pB = r'(\([0-9]{4}\))'
                pBarr = []
                pBLength = 0

                #p6 = r'(.*\([A-Za-z]+ .* [0-9]{4}[A-Za-z]{1}\)[^\.]+\.+?)'  # p6 ... (Chieu and Ng, 2002b) ...
                #p7 = r'(.*\([A-Za-z]+ .* [0-9]{4}[A-Za-z]{1}+\)\.)'  # p7 ...(Chieu and Ng, 2002b).
                #for above cases:
                pC = r'(\([A-Za-z\, ]+[0-9]{4}[A-Za-z]{1}\))'
                pCarr = []
                pCLength = 0

                #p4 = r'(.*\[[0-9]{1,4}\][^\.]+\.)'                  # p4 ... Arthur [9]... & #.. that Waren and Pereira [2009] but .... .
                #for above case:
                pD = r'([A-Za-z]* \[[0-9]{1,4}\])'      #pB mdify hogi issay yey Arthur(2009) not only (2009)
                pDarr = []
                pDLength = 0

                #p5 = r'(.*\[[0-9]{1,3}.*\][^\.]*\.)'                # p5 ... IEE (eg: ....[4,3,...]....) (Multi)
                #for above case:
                pE = r'(\[[0-9 \,]+\])'
                pEarr = []
                pELength = 0

                #Case : There exists stack decoding algorithm (Berger et al., 1996;), A* search algorithm
                # (Och et al., 2001; Wang and Waibel, 1997) and dynamic-programming algorithms
                # (Tillmann and Ney, 2000; GarciaVarea and Casacuberta, 2001), and all translate a given input string
                #for above case:
                pF = r'(\([A-Za-z. \,]+[0-9]{4}+;?\)?)'
                pFarr = []
                pFLength = 0

                #tt = "One can either (Tsarfaty, 2006; Cohen and Smith, 2007; Goldberg and Tsarfaty, 2008; Green and Manning, 2010)."
                #CARA_2
                pG = r'(\(?[A-Za-z \,]+[0-9]{4}+;?\)?)'     #Less errors
                #CARA_3
                #pG = r'(\(?[A-Za-z]+\, [0-9]{4}+;?\)?)'    #"Use this to avoid getting hit on 2001, but increases exceptions and other probs"
                pGarr = []
                pGLength = 0

                #tt = "For a discussion of recent Chinese {9210) segmentation work, see Sproat et al. {1996)."
                pH = r'(\{[0-9]{4}\))'
                pHarr = []
                pHLength = 0

                #tt = "Named Entity instances in a large (Dani 19) un-annotated corpus (Sekine 05)."
                pI = r'(\([A-Za-z ]+ [0-9]{2}+\))'
                pIarr = []
                pILength = 0

                #tt = "Rosti et al.(2007b) partially resolved the problem."
                pJ = r'(\([0-9]{4}[A-Za-z]{1}\))'
                pJarr = []
                pJLength = 0

                #print("Citance : " + str(preSentenceList[0]))

                pAarr = re.findall(pA, str(preSentenceList[0]))
                pBarr = re.findall(pB, str(preSentenceList[0]))
                pCarr = re.findall(pC, str(preSentenceList[0]))
                pDarr = re.findall(pD, str(preSentenceList[0]))
                pEarr = re.findall(pE, str(preSentenceList[0]))
                pFarr = re.findall(pF, str(preSentenceList[0]))
                pGarr = re.findall(pG, str(preSentenceList[0]))
                pHarr = re.findall(pH, str(preSentenceList[0]))
                pIarr = re.findall(pI, str(preSentenceList[0]))
                pJarr = re.findall(pJ, str(preSentenceList[0]))


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

                if(tempMax != 0):
                    totalCount+=1

                #print("Max is : " + str(tempMax))
                if(tempMax == pFLength):
                    print("******************************************************")

                if(tempMax == 0):
                    citanceCategory = "Exception"
                elif(tempMax == 1):
                    citanceCategory = "Single Citance"
                elif(tempMax > 1):
                    citanceCategory = "Multi Citance"

                if(categoryCounterForContiguous == tempCitanceNumber):
                   arr = list(set(matchingSid) - set(tempListConti))
                   print(matchingSid)
                   print("arr : " + str(arr))
                   print(tempListConti)
                   if(str(arr) < tempListConti[len(tempListConti)-1]):
                       citanceCategory = "Pre Contiguous"
                   else:
                       citanceCategory = "Post Contiguous"
                tempCitanceNumber += 1
                csvWriter.writerow(
                    [tempCitanceNumber, refrencePaper, citingPaper,
                    preSentenceList[2], preSentenceList[1],
                    preSentenceList[0],
                    postSentenceList[0], postSentenceList[1],
                    citanceCategory])

                tempPreSentencesCount = 0
                tempPreSentences = []

                citanceCategory = ""
                tempPre1Sentece = ""

                tree = None
                root = None
                stopCondition = False
            except ParseError:
                #print("Error In Folder: " + folder + "Citing Paper:" + citingPaper)
                errorCount+=1
        #print(dataDict[5])
        dataDict = []
        print("Total Count is : " + str(totalCount))
        aaa+=1
        if(aaa == 5):
            break
