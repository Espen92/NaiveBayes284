import math
import os
import numpy as np
import json

import tkinter
from tkinter import filedialog
from collections import Counter

import NaiveBayesFunctions as nb
from interface_functions import print_inline

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


class NaiveBayes:
    def __init__(self):
        self.posTestReviewsList = None
        self.negTestReviewsList = None
        self.probs = None
        self.zeroV = None
        self.emptyPos = None
        self.emptyNeg = None

        print("choose your 'test' folder")
        tkinter.Tk().withdraw()
        self.testDirPath = filedialog.askdirectory()

    def set_review_list(self):
        if self.posTestReviewsList is not None and self.negTestReviewsList is not None:
            return
        
        self.posTestReviewsList, self.negTestReviewsList = nb.createArrayList(
            self.testDirPath)

    def loadData(self):
        """
        Lets the user choose what folders to load train and test data from and creates
        lists of reviews and dictionaries of word frequencies. The choosen folders must
        have subfolders named pos and neg.
        """

        print("choose your 'train' folder")
        tkinter.Tk().withdraw()
        folderpath = filedialog.askdirectory()


        posList, negList = nb.createArrayList(folderpath)
        print("made the lists")
        # lager dictionaries med antall reviews disse ordene forekommer i (ut av de positive/negative)
        negWordsDict = nb.addWords(negList)
        posWordsDict = nb.addWords(posList)
        allWords = Counter(negWordsDict) + Counter(posWordsDict)
        print("made the dicts")

        self.set_review_list()
        print("loading done, type 'help' for helpfull commands")

        pListLeng = len(posList)
        nListLeng = len(negList)
        self.probs, self.zeroV, self.emptyPos, self.emptyNeg = nb.preProb(posWordsDict, pListLeng,
                                                      negWordsDict, nListLeng, allWords)

    def saveData(self):
        if (self.probs is None or self.zeroV is None
                or self.emptyPos is None or self.emptyNeg is None):
            print("Generate or import model before saving model!")
            return
            
        values = {"probs": self.probs,
                  "zeroV": self.zeroV,
                  "emptyPos": self.emptyPos,
                  "emptyNeg": self.emptyNeg}

        with open(os.path.join(__location__, "preset_model.json"), "w") as outfile:
            json.dump(values, outfile)

    def load_data_from_file(self):
        self.set_review_list()
        with open(os.path.join(__location__, "preset_model.json"), "r") as data:
            j_data = json.load(data)

            self.probs = j_data.get("probs", None)
            self.zeroV = j_data.get("zeroV", None)
            self.emptyPos = j_data.get("emptyPos", None)
            self.emptyNeg = j_data.get("emptyNeg", None)

    def score(self):
        """
        Goes through every review in the test folder and attempts to classify it. 
        Then checks if the classification was right or not and updates the score 
        accordingly. Finally displays the score.
        """

        if (self.probs is None or self.zeroV is None 
                or self.emptyPos is None or self.emptyNeg is None):
            print("Generate or import model before running score!")
            return

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

        if (self.probs is None or self.zeroV is None
                or self.emptyPos is None or self.emptyNeg is None):
            print("Generate or import model before running classify!")
            return

        review_list = np.array(review.split())
        neg, pos = nb.getProbs(review_list, self.probs, self.zeroV, self.emptyPos, self.emptyNeg)
        if neg > pos:
            print("Your review is negative")
        else:
            print("Your review is positive")
