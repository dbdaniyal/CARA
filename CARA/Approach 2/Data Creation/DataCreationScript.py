import json
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
import csv

path="E:/DSU Semesters/8th Semester/CS-412 FYP/Data/Training-Set-2019/Task1/From-ScisummNet-2019"
path=os.path.realpath(path)
# Fetch directory list from folder
directoryList = os.listdir(path)
csvFileObj = open('CARA_2019_CleanText.csv', 'w', newline='')
csvWriter = csv.writer(csvFileObj)

# Headers of CARA csv file
csvWriter.writerow(["rowCount","citanceNumber","mainFolderCount","referenceArticle","citingArticle","refAnnotatedOffsets",
                    "citationSentence", "citingPaperAuthor"])

#id = 0                  #ref article ID, made this to avoid storing whole ref paper text to each and evry entry of a ref paper for all citing papers
csvRowCount = 0            #count of rows of csv file
mainFolderCount = 0

for folder in directoryList:
    referencePaperText = []  # it contains full text of a reference paper in array form, at each index 1 sentence is stored, so full array contains whole data of 1 paper
    citanceNo = ""
    citingPaperId = ""
    citance = ""
    citingPaperAuthors = ""
    refAnnotatedSentence = []       #to store reference sentence from annotated txt to csv
    refAnnCounter = 0
    dictCounter = 0
    dictName= []

    refPaperPath = os.path.join(path, folder+"\\Reference_XML")
    refPaperFolderName = os.listdir(refPaperPath) #contains folder name
    refPaperXMLFile = os.path.join(refPaperPath,refPaperFolderName[0])

    annotatedFilePath = os.path.join(path, folder+"\\annotation\\")
    annotatedFileName = os.listdir(annotatedFilePath)
    annotatedTXTFile = os.path.join(annotatedFilePath,annotatedFileName[0])

    with open(annotatedTXTFile, encoding="utf8") as annFileData:
        annotatedList = annFileData.readlines()  # contains exact copy of c00-2123.ann.txt in list form
        annotatedModifiedArray = []  # contains final modified and cleaned form of each annotation
        count = 0

        for eachLine in annotatedList:      #cleansing
            if (eachLine != '\n'):  # to remove line breaks in from overall data(all lines)
                eachLine = eachLine.replace('\n', '')  # to remove line breaks within a data (line)
                annotatedModifiedArray.insert(count, eachLine)
                count += 1

        #extracting reference offsets
        dictCounter = 0
        for eachLine in annotatedModifiedArray:
            splittedArr = eachLine.split(' | ')

            if(len(splittedArr) == 11):
                temp1 = splittedArr[7].split(':')
                temp2 = temp1[1].lstrip()
                temp3 = temp2.split(',')

                k = 0
                removalChars = " []\'"
                while (k != len(temp3)):
                    for char in removalChars:
                        temp3[k] = temp3[k].replace(char, '')
                    refAnnotatedSentence.insert(refAnnCounter, temp3[k])
                    refAnnCounter += 1
                    k+=1
                dictName.insert(dictCounter,refAnnotatedSentence)
                #print(dictCounter)
                dictCounter+=1
            else:
                dictName.insert(dictCounter, "$")
                dictCounter+=1
            refAnnotatedSentence = []
            #dictName = {dictCounter:refAnnotatedSentence}
    #print(refAnnotatedSentence)
    dictCounter = 0         #again equating it with 0 to store offsets in csv
    with open(refPaperXMLFile) as refFileData:
        #annotatedList = refFileData.readlines()  # line by line fetch data
        #print(annotatedList)
        #folderName = folderName.split(".xml")  # In CSV the file name is written i.e C00-2123.xml after splitting C00-2123
        #folderName = str(folderName[0])

        try:
            tree = ET.parse(refPaperXMLFile)
            root = tree.getroot()
            count = 0
            for child in root:
                for data in root.iter('S'):
                    Sid = data.get('sid')
                    sentenceOnSid = data.text.encode('UTF-8')
                    sentenceOnSid = str(sentenceOnSid)
                    sentenceOnSid = sentenceOnSid.replace("b\'","")
                    sentenceOnSid = sentenceOnSid.replace("b\"","")
                    referencePaperText.insert(count, sentenceOnSid)
                    count += 1
                break
        except ParseError:
            print("**EXCEPTION**")

    citinSentecePath = os.path.join(path, folder+"\\citing_sentences.json")
    with open(citinSentecePath) as json_file:
        data = json.load(json_file)
        for p in data:
            citanceNo = (p['citance_No'])
            citingPaperId = (p['citing_paper_id'])

            citance = str((p['clean_text']).encode("utf-8"))
            citance = citance.replace("b\'", "")
            citance = citance.replace("b\"", "")
            citingPaperAuthors = str((p['citing_paper_authors']).encode("utf-8"))
            citingPaperAuthors = citingPaperAuthors.replace("b\'","")
            if(citance != '\''):
                csvWriter.writerow([csvRowCount,citanceNo,mainFolderCount,refPaperFolderName[0],citingPaperId, dictName[dictCounter],citance,citingPaperAuthors])
                csvRowCount+=1
            #print(dictCounter)
            dictCounter+=1
    print(str(refPaperFolderName[0]))
    mainFolderCount+=1