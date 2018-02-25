#%%
import os
import numpy as np
import jupyter
import math


def getTrainData(trainDataFolder):
    return os.listdir(trainDataFolder)


neg = "C:\\Users\\Espen\\INFO284\\Exam1\\aclImdb\\train\\neg\\"
pos = "C:\\Users\\Espen\\INFO284\\Exam1\\aclImdb\\train\\pos\\"
negativeData = getTrainData(neg)
positiveData = getTrainData(pos)


#%%


def createArrayList(posDat, path):
    theList = []
    for flie in posDat:
        with open(path+flie, encoding='utf8') as f:
            text = f.readlines()
            wordsarray = np.genfromtxt(
                text, case_sensitive="lower", deletechars='.,!?()', dtype=str)

            theList.append(wordsarray)
    return theList


posList = createArrayList(positiveData, pos)


#%%
negList = createArrayList(negativeData, neg)

#%%


def addWords(theList):
    dic = {}
    for each in theList:
        if (each.shape == ()):
            each = np.array([""])
        for every in each:
            if every in dic:
                dic[every] += 1
            else:
                dic[every] = 1
    return dic


negWordsDict = addWords(negList)
posWordsDict = addWords(posList)


#%%


def getDeltas(wordsDict1, wordsDict2):

    deltas = {}

    for x in wordsDict1:
        if x in wordsDict2:
            delta = math.fabs(wordsDict1[x] - wordsDict2[x])
            if wordsDict2[x] < wordsDict2.__len__() / 3:
                deltas[x] = delta
        else:
            delta = wordsDict1[x]
            deltas[x] = delta

    for y in wordsDict2:
        if y in wordsDict1 and y not in deltas:
            delta = math.fabs(wordsDict1[y] - wordsDict2[y])
            if wordsDict1[y] < wordsDict1.__len__() / 3:
                deltas[y] = delta
        elif y not in deltas:
            delta = wordsDict2[y]
            deltas[y] = delta

    return deltas


theDeltas = getDeltas(negWordsDict, posWordsDict)

#%%
print(posWordsDict.__len__())
print(negWordsDict.__len__())
print(theDeltas.__len__())
median = 1


def halveDict(myDic, median):
    newDict = {}
    deltaList = []
    for delta in theDeltas:
        if theDeltas[delta] > median:
            newDict[delta] = theDeltas[delta]
            deltaList.append(theDeltas[delta])

    newMedian = np.median(deltaList)
    print(median)
    return newDict, newMedian


while (theDeltas.__len__() > 1000):
    theDeltas, median = halveDict(theDeltas, median)

#%%
givenPosProbOfWord = {}
givenNegProbOfWord = {}
for x in theDeltas:
    prN = (negWordsDict[x] / negWordsDict.__len__())
    givenNegProbOfWord[x] = prN
    prP = (posWordsDict[x] / posWordsDict.__len__())
    givenPosProbOfWord[x] = prN
    print(prN, prP)

# endre så vi teller antall reviews som inneholder ordet, ikke antall forekomster av ordet
