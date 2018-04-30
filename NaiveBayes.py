import tkinter
from tkinter import filedialog
import numpy as np
import NaiveBayesFunctions as nb
from collections import Counter
import math
from interface_functions import print_inline

class NaiveBayes:
    def __init__(self):
        self.posTestReviewsList = None
        self.negTestReviewsList = None

        self.probs = None
        self.zeroV = None
        self.emptyPos = None
        self.emptyNeg = None


    def loadData(self):
        """
        Lets the user choose what folders to load train and test data from and creates
        lists of reviews and dictionaries of word frequencies. The choosen folders must
        have subfolders named pos and neg.
        """

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

        self.posTestReviewsList, self.negTestReviewsList = nb.createArrayList(testDirPath)
        print("loading done, type 'help' for helpfull commands")

        pListLeng = len(posList)
        nListLeng = len(negList)
        self.probs, self.zeroV, self.emptyPos, self.emptyNeg = nb.preProb(posWordsDict, pListLeng,
                                                      negWordsDict, nListLeng, allWords)

    def score(self):
        """
        Goes through every review in the test folder and attempts to classify it. 
        Then checks if the classification was right or not and updates the score 
        accordingly. Finally displays the score.
        """
        gotItRight = 0
        counter = 0

        for rev in self.posTestReviewsList:
            counter += 1
            neg, pos = nb.getProbs(rev, self.probs, self.zeroV, self.emptyPos, self.emptyNeg)
            if pos > neg:
                gotItRight += 1
            if counter % 1000 == 0:
                dots = counter//1000 % 4
                print_inline("working", dots*".")
        for rev in self.negTestReviewsList:
            counter += 1
            neg, pos = nb.getProbs(rev, self.probs, self.zeroV, self.emptyPos, self.emptyNeg)
            if pos < neg:
                gotItRight += 1
            if counter % 1000 == 0:
                dots = counter//1000 % 4
                print_inline("working", dots*".")
        print(f"score {gotItRight/counter}")


    def classify(self, review):
        """
        attempts to classify a review submited by a user and prints if 
        it is posive or negative
        """
        review_list = np.array(review.split())
        neg, pos = nb.getProbs(review_list, self.probs, self.zeroV, self.emptyPos, self.emptyNeg)
        if neg > pos:
            print("Your review is negative")
        else:
            print("Your review is positive")
