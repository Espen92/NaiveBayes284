import os
import numpy as np
from collections import Counter
import math
from string import punctuation

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


def createArrayList2(path):
    pos_list = []
    neg_list = []
    neg = os.listdir(path+"\\neg\\")
    pos = os.listdir(path+"\\pos\\")
    table = str.maketrans('', '', punctuation)
    for file_ in neg:
        with open(path+"\\neg\\"+file_, encoding='utf-8') as f:
            text = f.read().lower()
            cleanText = text.translate(table)
            wordsarray = np.array(cleanText.split())
            neg_list.append(wordsarray)

    for file_ in pos:
        with open(path+"\\pos\\"+file_, encoding='utf-8') as fi:
            text = fi.read().lower()
            cleanText = text.translate(table)
            wordsarray = np.array(cleanText.split())
            pos_list.append(wordsarray)
    return pos_list, neg_list


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
def preProb(poswordsDict, poslisLen, negwordsDict, neglisLen, allWords):
    print("")
    allWLeng = len(allWords)
    new_dict = {}
    emptyPosProb = math.log(0.5)
    emptyNegProb = math.log(0.5)
    for word in allWords:
        x = (math.log(((negwordsDict[word]+1)/(allWLeng+neglisLen))), math.log(((poswordsDict[word]+1)/(allWLeng+poslisLen))),
             math.log((1-((negwordsDict[word]+1)/(allWLeng+neglisLen)))),     math.log((1-((poswordsDict[word]+1)/(allWLeng+poslisLen)))))
        new_dict[word] = x
        emptyNegProb += x[2]
        emptyPosProb += x[3]
    firstTimeValue = (math.log(1/(allWLeng+neglisLen)), math.log(1/(allWLeng+poslisLen)),
                      math.log(1-(1/(allWLeng+neglisLen))), math.log(1-(1/(allWLeng+poslisLen))))

    return new_dict, firstTimeValue, emptyPosProb, emptyNegProb


def prob(review, probsDict, firstTimeValue, emptyPosProb, emptyNegProb):
    if review.shape != ():
        for word in review:
            if word not in probsDict:
                probsDict[word] = firstTimeValue
                emptyPosProb += firstTimeValue[1]
                emptyNegProb += firstTimeValue[0]
            else:
                wProbs = probsDict[word]
                emptyNegProb += (wProbs[0] - wProbs[2])
                emptyPosProb += (wProbs[1] - wProbs[3])

    return emptyPosProb, emptyNegProb


def prob2(review, probsDict, firstTimeValue):
    currentNegP = math.log(0.5)
    currentPosP = math.log(0.5)
    for word in review:
        if word not in probsDict:
            probsDict[word] = firstTimeValue
    for word in probsDict:
        wordProbs = probsDict[word]
        if word in review:
            currentNegP += wordProbs[0]
            currentPosP += wordProbs[1]
        else:
            currentNegP += wordProbs[2]
            currentPosP += wordProbs[3]
    return currentPosP, currentNegP


def getProbs(review, probs, zeroV, emptyPosProb, emptyNegProb):
    po, ne = prob(review, probs, zeroV, emptyPosProb, emptyNegProb)
    probOfPos = po/(po+ne)
    probOfNeg = ne/(po+ne)
    return probOfPos, probOfNeg
