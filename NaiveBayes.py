import tkinter
from tkinter import filedialog
import numpy as np
import NaiveBayesFunctions as nb
from collections import Counter
import math
from cli_Stuff import print_inline

posList = None
negList = None
negWordsDict = None
posWordsDict = None
allWords = None
posTestReviewsList = None
negTestReviewsList = None


def loadData():
    """
    Lets the user choose what folders to load train and test data from and creates
    lists of reviews and dictionaries of word frequencies. The choosen folders must
    have subfolders named pos and neg.
    """
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
    print("choose your 'test' folder")
    tkinter.Tk().withdraw()
    testDirPath = filedialog.askdirectory()
    # lager en liste av de positive og en av de negative
   # posList = nb.createArrayList(positiveData, pos)
   # negList = nb.createArrayList(negativeData, neg)
    posList, negList = nb.createArrayList(folderpath)
    print("made the lists")
    # lager dictionaries med antall reviews disse ordene forekommer i (ut av de positive/negative)
    negWordsDict = nb.addWords(negList)
    posWordsDict = nb.addWords(posList)
    allWords = Counter(negWordsDict) + Counter(posWordsDict)
    print("made the dicts")

    posTestReviewsList, negTestReviewsList = nb.createArrayList(testDirPath)
    print("loading done, type 'help' for helpfull commands")


def score():
    """
    Goes through every review in the test folder and attempts to classify it. 
    Then checks if the classification was right or not and updates the score 
    accordingly. Finally displays the score.
    """
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
            print_inline("working", dots*".")
    for rev in negTestReviewsList:
        counter += 1
        neg, pos = nb.getProbs(rev, probs, zeroV, emptyPos, emptyNeg)
        if pos < neg:
            gotItRight += 1
        if counter % 1000 == 0:
            dots = counter//1000 % 4
            print_inline("working", dots*".")
    print(f"score {gotItRight/counter}")


def classify(review):
    """
    attempts to classify a review submited by a user and prints if 
    it is posive or negative
    """
    review_list = np.array(review.split())
    pListLeng = len(posList)
    nListLeng = len(negList)
    probs, zeroV, emptyPos, emptyNeg = nb.preProb(posWordsDict, pListLeng,
                                                  negWordsDict, nListLeng, allWords)
    neg, pos = nb.getProbs(review_list, probs, zeroV, emptyPos, emptyNeg)
    if neg > pos:
        print("Your review is negative")
    else:
        print("Your review is positive")
