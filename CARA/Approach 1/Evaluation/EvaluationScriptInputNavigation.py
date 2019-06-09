import csv
import matplotlib.pyplot as plt
from pip._vendor.distlib.compat import raw_input
from sklearn.metrics import confusion_matrix
import numpy as np
import regex as re
import statistics
from sklearn.metrics import average_precision_score
from sklearn.metrics import classification_report

def plot_confusion_matrix(y_true, y_pred, classes,
                          # normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    # if not title:
    #     if normalize:
    #         title = 'Normalized confusion matrix'
    #     else:
    #         title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    #print(classes)
    #classes = classes[unique_labels(y_true, y_pred)]
    #print(classes)
    # if normalize:
    #     cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    #     print("Normalized confusion matrix")
    # else:
    #     print('Confusion matrix, without normalization')

    print(cm)
    headers = ['Multi Citance' ,'Post Contiguous','Pre Contiguous','Single Citance']
    csvFile = open('CitationCategoryEvaluation.csv', 'w', newline='')
    # Use csv Writer
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(headers)
    for eachRow in cm:
        csvWriter.writerow([eachRow[0] , eachRow[1] , eachRow[2] , eachRow[3]])

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    # fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j]),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax

def citanceCategoryFunc(citance):
    strCitanceCategory = ""
    """
    Single Citance:                 main sentence that has a citation point
    Multi Citance:                  refers to a citing sentence that has multiple citation points within one sentence
    Contiguous-sentence citation:   refers to a multiple sentence citation with preceding or forgoing sentences(s) of citing sentence.
    Multi-sentence citation:        refers to citation text that may or may not be contiguous. 
    """

    # p1 = r'(.*\([A-Za-z]+ .* [0-9]{4}+\)\.+?)'          # p1 ... says that (Warren and Pereira, 1982).
    # p2 = r'(.*\([A-Za-z]+ .* [0-9]{4}+\)[^\.]+\.+?)'    # p2 ... says that (Warren and Pereira, 1982) but ... .
    # p8 = r'(.*\([A-Za-z\,]+ [0-9]{4}+\)\.+?)'  # p8 ... says that (Pereira, 1982).
    # p9 = r'(.*\([A-Za-z\,]+ [0-9]{4}+\)[^\.]+\.+?)'  # p9 ... says that (Pereira, 1982)....
    # for above cases:
    pA = r'(\([A-Za-z\, ]+ [0-9]{4}+\))'
    pAarr = []
    pALength = 0

    # p3 = r'(.*\([0-9]{4}\).*\.)'  # p3 ... that Waren and Pereira (2009) but .... .
    # for above case:
    pB = r'(\([0-9]{4}\))'
    pBarr = []
    pBLength = 0

    # p6 = r'(.*\([A-Za-z]+ .* [0-9]{4}[A-Za-z]{1}\)[^\.]+\.+?)'  # p6 ... (Chieu and Ng, 2002b) ...
    # p7 = r'(.*\([A-Za-z]+ .* [0-9]{4}[A-Za-z]{1}+\)\.)'  # p7 ...(Chieu and Ng, 2002b).
    # for above cases:
    pC = r'(\([A-Za-z\, ]+[0-9]{4}[A-Za-z]{1}\))'
    pCarr = []
    pCLength = 0

    # p4 = r'(.*\[[0-9]{1,4}\][^\.]+\.)'                  # p4 ... Arthur [9]... & #.. that Waren and Pereira [2009] but .... .
    # for above case:
    pD = r'([A-Za-z]* \[[0-9]{1,4}\])'  # pB mdify hogi issay yey Arthur(2009) not only (2009)
    pDarr = []
    pDLength = 0

    # p5 = r'(.*\[[0-9]{1,3}.*\][^\.]*\.)'                # p5 ... IEE (eg: ....[4,3,...]....) (Multi)
    # for above case:
    pE = r'(\[[0-9 \,]+\])'
    pEarr = []
    pELength = 0

    # Case : There exists stack decoding algorithm (Berger et al., 1996;), A* search algorithm
    # (Och et al., 2001; Wang and Waibel, 1997) and dynamic-programming algorithms
    # (Tillmann and Ney, 2000; GarciaVarea and Casacuberta, 2001), and all translate a given input string
    # for above case:
    pF = r'(\([A-Za-z. \,]+[0-9]{4}+;?\)?)'
    pFarr = []
    pFLength = 0

    # tt = "One can either (Tsarfaty, 2006; Cohen and Smith, 2007; Goldberg and Tsarfaty, 2008; Green and Manning, 2010)."
    # CARA_2
    pG = r'(\(?[A-Za-z \,]+[0-9]{4}+;?\)?)'  # Less errors
    # CARA_3
    # pG = r'(\(?[A-Za-z]+\, [0-9]{4}+;?\)?)'    #"Use this to avoid getting hit on 2001, but increases exceptions and other probs"
    pGarr = []
    pGLength = 0

    # tt = "For a discussion of recent Chinese {9210) segmentation work, see Sproat et al. {1996)."
    pH = r'(\{[0-9]{4}\))'
    pHarr = []
    pHLength = 0

    # tt = "Named Entity instances in a large (Dani 19) un-annotated corpus (Sekine 05)."
    pI = r'(\([A-Za-z ]+ [0-9]{2}+\))'
    pIarr = []
    pILength = 0

    # tt = "Rosti et al.(2007b) partially resolved the problem."
    pJ = r'(\([0-9]{4}[A-Za-z]{1}\))'
    pJarr = []
    pJLength = 0

    #print("Citance : " + str(citance))

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
    if (tempMax == 0):
        return 0
    elif (tempMax == 1):
        return 1
    elif (tempMax > 1):
        return 2


def compareScores(preOneAndCitation , citationAndPostOne):
    if(preOneAndCitation > citationAndPostOne):
        return "Pre"
    else:
        return "Post"

file = open("DataForSimilarity.csv", 'r', encoding="utf-8")
reader = csv.reader(file)
DictOfCara = []
DictOfResults = []
tt=0
exceptionList = []
counter = 0
for line in reader:
    if(tt > 0):  # bcz in row 0 headings are written (citationSntence, refrenceArticle, ...)
        if(line[8] != 'Exception'):
            DictOfCara.insert(tt, {'citanceNumber': line[0], 'referenceArticle': line[1],
                                  'citingArticle': line[2],'preTwo':line[3],
                                  'preOne':line[4], 'citationSentence':line[5],
                                    'postOne':line[6], 'postTwo':line[7] , 'citationCategory':line[8]})
        else:
            exceptionList.insert(counter,line[0])
            #print(line[8])
            #print(line[0])
            counter += 1
    tt+=1
print(len(DictOfCara))
input = raw_input("Enter Similarity Score Code: ")
tt = 0
fileName = ""
if(input == "co"):
    fileName = "Approach_1_Cosine.csv"
elif(input == "eu"):
    fileName = "Approach_1_Eucledian.csv"
elif(input == "ja"):
    fileName = "Approach_1_Jaccard.csv"
elif(input == "mi"):
    fileName = "Approach_1_Minkowski.csv"
elif(input == "ma"):
    fileName = "Approach_1_Manhattan.csv"

resultCsv = open(fileName, 'r')
reader = csv.reader(resultCsv)
counter = 0

listOfCitationScore = []
listOfPreOneScore = []
listOfPostOneScore = []
listOfPreOneAndCitationScore = []
listOfPostOneAndCitationScore = []
for line in reader:
    if(tt > 0):
        DictOfResults.insert(tt, {'citanceNumber': line[0], 'preTwo': line[1],'preOne': line[2],
                                'citationSentence': line[3],'postOne': line[4], 'postTwo': line[5],
                                'preoneAndCitation': line[6], 'citationAndPostOne': line[7],
                                'citingArticle': line[8], 'referenceArticle': line[9], 'length': line[10]})

    tt+=1
print(len(DictOfResults))
citationCategoryListActual = [] # actual category list

i = 0
while i < len(DictOfCara):
    #citationScoreList.insert(i , float(DictOfResults[i].get('citationSentence')))
    category = DictOfCara[i].get('citationCategory')
    #categoryCitation = citanceCategoryFunc(DictOfCara[i].get('citationSentence'))
    citationCategoryListActual.insert(i,category)

    listOfCitationScore.insert(i, float(DictOfResults[i].get('citationSentence')))
    listOfPreOneScore.insert(i, float(DictOfResults[i].get('preOne')))
    listOfPostOneScore.insert(i, float(DictOfResults[i].get('preTwo')))
    listOfPreOneAndCitationScore.insert(i, float(DictOfResults[i].get('preoneAndCitation')))
    listOfPostOneAndCitationScore.insert(i, float(DictOfResults[i].get('citationAndPostOne')))
    i+=1

#meanOfCitationScore = round(statistics.mean(citationScoreList),3)
# print("Mean :" + str(meanOfCitationScore))
# print("median :" + str(round(statistics.median(citationScoreList),3)))
# print("sd :" + str(round(statistics.stdev(citationScoreList),3)))
# print("sd :" + str(4*round(statistics.stdev(citationScoreList),3) + meanOfCitationScore))

i = 0
count = []
c1 = 0

citationCategoryPredicted = []
meanOfCitationScore = round(statistics.mean(listOfCitationScore),3)
stdAndmeanOfCitationScore = (3*round(statistics.stdev(listOfCitationScore),3))+ meanOfCitationScore
stdOfCitataionScore = round(statistics.stdev(listOfCitationScore),3)
print("Citation Sentence : ")
print("Mean :" + str(meanOfCitationScore))
print("sd :" + str(round(statistics.stdev(listOfCitationScore),3)))
print("sd and mean :" + str(4*round(statistics.stdev(listOfCitationScore),3) + meanOfCitationScore))
print()

meanOfPreOneScore = round(statistics.mean(listOfPreOneScore),3)
stdAndmeanOfPreScore = (3*round(statistics.stdev(listOfPreOneScore),3))+ meanOfPreOneScore
stdOfPreOneScore = round(statistics.stdev(listOfPreOneScore),3)
print("Pre One : ")
print("Mean :" + str(meanOfPreOneScore))
print("sd :" + str(round(statistics.stdev(listOfPreOneScore),3)))
print("sd and mean :" + str(4*round(statistics.stdev(listOfPreOneScore),3) + meanOfPreOneScore))
print()

meanOfPostOneScore = round(statistics.mean(listOfPostOneScore),3)
stdAndmeanOfPostOneScore = (3*round(statistics.stdev(listOfPostOneScore),3))+ meanOfPostOneScore
stdOfPostOneScore = round(statistics.stdev(listOfPostOneScore),3)
print("Citation Sentence : ")
print("Mean :" + str(meanOfPostOneScore))
print("sd :" + str(round(statistics.stdev(listOfPostOneScore),3)))
print("sd and mean :" + str(4*round(statistics.stdev(listOfPostOneScore),3) + meanOfPostOneScore))
print()

meanOfPreOneAndCitationScore = round(statistics.mean(listOfPreOneAndCitationScore),3)
stdAndmeanOfPreOneAndCitationScore = (3*round(statistics.stdev(listOfPreOneAndCitationScore),3))+ meanOfPreOneAndCitationScore
stdOfPreOneAndCitationScore = round(statistics.stdev(listOfPreOneAndCitationScore),3)
print("Citation Sentence : ")
print("Mean :" + str(meanOfPreOneAndCitationScore))
print("sd :" + str(round(statistics.stdev(listOfPreOneAndCitationScore),3)))
print("sd and mean :" + str(4*round(statistics.stdev(listOfPreOneAndCitationScore),3) + meanOfPreOneAndCitationScore))
print()

meanOfPostOneAndCitationScore = round(statistics.mean(listOfPostOneAndCitationScore),3)
stdAndmeanOfPostOneAndCitationScore = (3*round(statistics.stdev(listOfPostOneAndCitationScore),3))+ meanOfPostOneAndCitationScore
stdOfPostOneAndCitationScore = round(statistics.stdev(listOfPostOneAndCitationScore),3)
print("Citation Sentence : ")
print("Mean :" + str(meanOfPostOneAndCitationScore))
print("sd :" + str(round(statistics.stdev(listOfPostOneAndCitationScore),3)))
print("sd and mean :" + str(4*round(statistics.stdev(listOfPostOneAndCitationScore),3) + meanOfPostOneAndCitationScore))
print()

while i < len(DictOfResults):
    category = " "
    if (float(DictOfResults[i].get('preoneAndCitation')) >= (0.35*stdAndmeanOfCitationScore)):
            citationCategoryPredicted.insert(i, "Pre Contiguous")
    elif (float(DictOfResults[i].get('citationAndPostOne')) >= (0.35*stdAndmeanOfCitationScore)):
            citationCategoryPredicted.insert(i, "Post Contiguous")
    else:
        if(citanceCategoryFunc(DictOfCara[i].get('citationSentence')) == 1):
           citationCategoryPredicted.insert(i, "Single Citance")
        #elif(citanceCategoryFunc(DictOfCara[i].get('citationSentence')) == 2):
        else:
           citationCategoryPredicted.insert(i, "Multi Citance")
    i+=1

# while i < len(DictOfResults):
#     category = " "
#     if (float(DictOfResults[i].get('preoneAndCitation')) >= float(DictOfResults[i].get('citationAndPostOne'))):
#             citationCategoryPredicted.insert(i, "Pre Contiguous")
#     elif (float(DictOfResults[i].get('preoneAndCitation')) < float(DictOfResults[i].get('citationAndPostOne'))):
#             citationCategoryPredicted.insert(i, "Post Contiguous")
#     else:
#            citationCategoryPredicted.insert(i, "Single Citance")
#     i+=1


if(input == "co"):
    plot_confusion_matrix(citationCategoryListActual, citationCategoryPredicted,
         classes=['Multi Citance' ,'Post Contiguous','Pre Contiguous','Single Citance'],
         title='Confusion matrix, with Cosine similarity')
elif(input == "eu"):
    plot_confusion_matrix(citationCategoryListActual, citationCategoryPredicted,
                          classes=['Multi Citance', 'Post Contiguous', 'Pre Contiguous', 'Single Citance'],
                          title='Confusion matrix, with Euclidean')
elif(input == "ja"):
    plot_confusion_matrix(citationCategoryListActual, citationCategoryPredicted,
                          classes=['Multi Citance', 'Post Contiguous', 'Pre Contiguous', 'Single Citance'],
                          title='Confusion matrix, with Jaccard')
elif(input == "mi"):
    plot_confusion_matrix(citationCategoryListActual, citationCategoryPredicted,
                          classes=['Multi Citance', 'Post Contiguous', 'Pre Contiguous', 'Single Citance'],
                          title='Confusion matrix, with Minkowski')

elif(input == "ma"):
    plot_confusion_matrix(citationCategoryListActual, citationCategoryPredicted,
                          classes=['Multi Citance', 'Post Contiguous', 'Pre Contiguous', 'Single Citance'],
                          title='Confusion matrix, with Manhattan')


#confusion_matrix.plot()
print(classification_report(citationCategoryListActual, citationCategoryPredicted))
plt.show()