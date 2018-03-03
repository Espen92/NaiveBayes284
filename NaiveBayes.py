#%%
import os
import numpy as np
import jupyter
import math
from collections import Counter

# henter listen av filer


def getTrainData(trainDataFolder):
    return os.listdir(trainDataFolder)


neg = "..\\Data\\train\\neg\\"
pos = "..\\Data\\train\\pos\\"
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

#%%
# joins the dictionaries to create one with all registered words
allWords = Counter(negWordsDict) + Counter(posWordsDict)

# return the probability of a review boing of a given type, wordsDict is posWordsDict or negWordsDict
# theList is posList or negList


def prob(review, wordsDict, theList):

    currentP = 0.5  # start with the probability of a review being good or bad, here that is 50/50
    # if there is a new word in this review, add it to allWords with 0 occurances
    for word in review:
        if word not in allWords:
            allWords[word] = 0

    for word in allWords:
        # if the word is in any positive/negative review, get the likelyhood of that that word given that the review is pos/neg and
        # multiply it by the current probability
        # this way we get P(w[i]|y)*P(w[... i ... ]|y)
        if word in wordsDict:
            # first check if the word is in the wordDict, if it isn't that means
            # the probability of that word, given that y is 0
            if word in review:
                # if the word IS in the review, that attribute is True, so we take the prob of it
                currentP = currentP * (wordsDict[word]/theList.__len__())
            else:
                # if it isn't in the review, it is False, so we take the inverse of the P (1-p)
                currentP = currentP * (1-(wordsDict[word]/theList.__len__()))
        # otherwise the P(w[i]|y=1) is 0, we will revisit this so it'sæ not actually 0
        else:
            if word in review:
                currentP = currentP * 0
            else:
                currentP = currentP * (1-0)

    return currentP


# this is where we get the actual probabilities.
def probOfPositive(review):
    return prob(review, posWordsDict, posList) / (prob(review, posWordsDict,
                                                       posList) + prob(review, negWordsDict, negList))


def probOfNegative(review):
    return prob(review, negWordsDict, negList) / (prob(review, posWordsDict,
                                                       posList) + prob(review, negWordsDict, negList))


#%%
# test
myTestReview = ["very", "good", "horrible"]
probOfBad = probOfNegative(myTestReview)
probOfGood = probOfPositive(myTestReview)

print("Probability of review being good: ", probOfGood, "\n", "Probability of review being bad: ",
      probOfBad, "\n" "sum of probabilities: ", (probOfBad+probOfGood))
