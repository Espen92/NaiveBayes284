

import jupyter
import NaiveBayesFunctions as nb
from collections import Counter
import math
import pathlib

posList = None
negList = None
negWordsDict = None
posWordsDict = None
allWords = None
posTestReviewsList = None
negTestReviewsList = None


def loadData():
    global posList
    global negList
    global negWordsDict
    global posWordsDict
    global allWords
    global posTestReviewsList
    global negTestReviewsList
    neg = "..\\Data\\train\\neg\\"
    pos = "..\\Data\\train\\pos\\"
    negativeData = nb.getTrainData(neg)
    positiveData = nb.getTrainData(pos)
    print("got the paths")

    # lager en liste av de positive og en av de negative
    posList = nb.createArrayList(positiveData, pos)
    negList = nb.createArrayList(negativeData, neg)
    print("made the lists")
    # lager dictionaries med antall reviews disse ordene forekommer i (ut av de positive/negative)
    negWordsDict = nb.addWords(negList)
    posWordsDict = nb.addWords(posList)
    allWords = Counter(negWordsDict) + Counter(posWordsDict)
    print("made the dicts")

    testNeg = "..\\Data\\test\\neg\\"
    testPos = "..\\Data\\test\\pos\\"
    print("getting test data")
    posTestReviewsList = nb.createArrayList(nb.getTrainData(testPos), testPos)
    negTestReviewsList = nb.createArrayList(nb.getTrainData(testNeg), testNeg)

    print("loading done")


def score():
    gotItRight = 0
    counter = 0
    pListLeng = len(posList)
    nListLeng = len(negList)
    for rev in posTestReviewsList:
        counter += 1
        neg, pos = nb.getProbs(rev, posWordsDict, pListLeng,
                               nListLeng, negWordsDict, allWords)
        if pos > neg:
            gotItRight += 1
        print(neg, pos, (neg+pos))
        print(f"score {gotItRight/counter}")


def classify(review):
    pListLeng = len(posList)
    nListLeng = len(negList)
    neg, pos = nb.getProbs(review, posWordsDict, pListLeng,
                           nListLeng, negWordsDict, allWords)
    if neg > pos:
        print("Your review is negative")
    else:
        print("Your review is positive")

# test


def myTest():
    myTestReview = ["I", "liked", "it", "it", "was", "nice"]

    probOfGood = nb.probOfPositive(
        myTestReview, posWordsDict, len(posList), len(negList), negWordsDict, allWords)
    probOfBad = nb.probOfNegative(
        myTestReview, posWordsDict, len(posList), len(negList), negWordsDict, allWords)
    print("Probability of review being good: ", probOfGood, "\n", "Probability of review being bad: ",
          probOfBad, "\n" "sum of probabilities: ", (probOfBad+probOfGood))
