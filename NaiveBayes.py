import tkinter
from tkinter import filedialog


import NaiveBayesFunctions as nb
from collections import Counter
import math

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

    print("choose your 'Data' folder")
    tkinter.Tk().withdraw()
    filename = filedialog.askdirectory()
    neg = f"{filename}\\train\\neg\\"
    pos = f"{filename}\\train\\pos\\"
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

    testNeg = f"{filename}\\test\\neg\\"
    testPos = f"{filename}\\test\\pos\\"
    print("getting test data")
    posTestReviewsList = nb.createArrayList(nb.getTrainData(testPos), testPos)
    negTestReviewsList = nb.createArrayList(nb.getTrainData(testNeg), testNeg)

    print("loading done")


def score():
    gotItRight = 0
    counter = 0
    pListLeng = len(posList)
    nListLeng = len(negList)
    probs, zeroV, emptyPos, emptyNeg = nb.preProb(posWordsDict, pListLeng,
                                                  negWordsDict, nListLeng, allWords)
    for rev in posTestReviewsList:
        counter += 1
        neg, pos = nb.getProbs(rev, probs, zeroV, emptyPos, emptyNeg)
        if pos > neg:
            gotItRight += 1
        print(f"score {gotItRight/counter}")


def classify(review):
    pListLeng = len(posList)
    nListLeng = len(negList)
    probs, zeroV, emptyPos, emptyNeg = nb.preProb(posWordsDict, pListLeng,
                                                  negWordsDict, nListLeng, allWords)
    neg, pos = nb.getProbs(review, probs, zeroV, emptyPos, emptyNeg)
    if neg > pos:
        print("Your review is negative")
    else:
        print("Your review is positive")
