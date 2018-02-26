#%%
import os
import numpy as np
import jupyter
import math

# henter listen av filer


def getTrainData(trainDataFolder):
    return os.listdir(trainDataFolder)


neg = "C:\\Users\\Espen\\INFO284\\Exam1\\Data\\train\\neg\\"
pos = "C:\\Users\\Espen\\INFO284\\Exam1\\Data\\train\\pos\\"
negativeData = getTrainData(neg)
positiveData = getTrainData(pos)


#%%

# tar en liste med filnavn og path til filene og lager en liste av numpy arrays
# numpy arrayene inneholder hver enkelt ord i et review
# prøver også å slette alle puktum, ikke så farlig, take it or leave it
def createArrayList(data, path):
    theList = []
    for flie in data:
        with open(path+flie, encoding='utf8') as f:
            text = f.readlines()
            wordsarray = np.genfromtxt(
                text, case_sensitive="lower", deletechars='.', dtype=str)

            theList.append(wordsarray)
    return theList


# lager en liste av de positive og en av de negative
posList = createArrayList(positiveData, pos)
negList = createArrayList(negativeData, neg)

#%%

# tar inn en liste av words arrays og returnerer en dictionary som inneholder
# hvert ord som finnes i noe array i den listen som keys. Disse har verdier
# som tilsvarer antall reviews som inneholder det ordet


def addWords(theList):
    dic = {}
    for each in theList:
        tempDic = {}
        if (each.shape == ()):
            each = np.array([""])
        for every in each:
            if every not in tempDic:
                tempDic[every] = True
                if every in dic:
                    dic[every] += 1
                else:
                    dic[every] = 1
    return dic


negWordsDict = addWords(negList)
posWordsDict = addWords(posList)
