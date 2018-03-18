import tkinter
from tkinter import filedialog
import numpy as np

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

    print("choose your 'train' folder")
    tkinter.Tk().withdraw()
    folderpath = filedialog.askdirectory()

    # lager en liste av de positive og en av de negative
   # posList = nb.createArrayList(positiveData, pos)
   # negList = nb.createArrayList(negativeData, neg)
    posList, negList = nb.createArrayList2(folderpath)
    print("made the lists")
    # lager dictionaries med antall reviews disse ordene forekommer i (ut av de positive/negative)
    negWordsDict = nb.addWords(negList)
    posWordsDict = nb.addWords(posList)
    allWords = Counter(negWordsDict) + Counter(posWordsDict)
    print("made the dicts")

    print("choose your 'test' folder")
    tkinter.Tk().withdraw()
    testDirPath = filedialog.askdirectory()
    posTestReviewsList, negTestReviewsList = nb.createArrayList2(testDirPath)
    print("loading done, type 'help' for helpfull commands")


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
        if counter % 1000 == 0:
            dots = counter//1000 % 4
            print("working", dots*".")
    for rev in negTestReviewsList:
        counter += 1
        neg, pos = nb.getProbs(rev, probs, zeroV, emptyPos, emptyNeg)
        if pos < neg:
            gotItRight += 1
        if counter % 1000 == 0:
            dots = counter//1000 % 4
            print("working", dots*".")
    print(f"score {gotItRight/counter}")


def classify(review):
    review_list = np.array(review.split())
    print(type(review_list))
    pListLeng = len(posList)
    nListLeng = len(negList)
    probs, zeroV, emptyPos, emptyNeg = nb.preProb(posWordsDict, pListLeng,
                                                  negWordsDict, nListLeng, allWords)
    neg, pos = nb.getProbs(review_list, probs, zeroV, emptyPos, emptyNeg)
    if neg > pos:
        print("Your review is negative")
    else:
        print("Your review is positive")
