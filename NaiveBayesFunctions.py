import os
import numpy as np
from collections import Counter
import math


# henter listen av filer


def getTrainData(trainDataFolder):
    return os.listdir(trainDataFolder)

# tar en liste med filnavn og path til filene og lager en liste av numpy arrays
# numpy arrayene inneholder hver enkelt ord i et review


def createArrayList(data, path):
    theList = []
    for file_ in data:
        with open(path+file_, encoding='utf8') as f:
            text = f.readlines()
            wordsarray = np.genfromtxt(
                text, case_sensitive="lower", dtype=str)

            theList.append(wordsarray)
    return theList


# tar inn en liste av words arrays og returnerer en dictionary som inneholder
# hvert ord som finnes i noe array i den listen som keys. Disse har verdier
# som tilsvarer antall reviews som inneholder det ordet

def addWords(theList):
    dic = Counter()
    for eachReview in theList:
        tempDic = {}
        if (eachReview.shape == ()):
            eachReview = np.array([""])
        for everyWord in eachReview:
            if everyWord not in tempDic:
                tempDic[everyWord] = True
                if everyWord in dic:
                    dic[everyWord] += 1
                else:
                    dic[everyWord] = 1
    return dic

# return the probability of a review boing of a given type, wordsDict is posWordsDict or negWordsDict
# theList is posList or negList


def prob(review, wordsDict, lisLen, allWords):

    currentP = math.log(0.5)
    for word in review:
        if word not in allWords:
            allWords[word] = 0
    allWLeng = len(allWords)
    for word in allWords:
        if word in review:
            currentP = currentP + \
                math.log(((wordsDict[word]+1)/(allWLeng+lisLen)))
        else:
            currentP = currentP + \
                math.log((1-((wordsDict[word]+1)/(allWLeng+lisLen))))
    return currentP


def probOfPositive(review, posWordsDict, posListLeng, negListLeng, negWordsDict, allWords):
    po = prob(review, posWordsDict, posListLeng, allWords)
    ne = prob(review, negWordsDict, negListLeng, allWords)
    return ne/(po+ne)


def probOfNegative(review, posWordsDict, posListLeng, negListLeng, negWordsDict, allWords):
    po = prob(review, posWordsDict, posListLeng, allWords)
    ne = prob(review, negWordsDict, negListLeng, allWords)
    return po/(po+ne)


def getProbs(review, posWordsDict, posListLeng, negListLeng, negWordsDict, allWords):
    po = prob(review, posWordsDict, posListLeng, allWords)
    ne = prob(review, negWordsDict, negListLeng, allWords)
    probOfPos = ne/(po+ne)
    probOfNeg = po/(po+ne)
    return probOfPos, probOfNeg
