import os
import json

import tkinter
import numpy as np
from tkinter import filedialog
from collections import Counter

import NaiveBayesFunctions as nb

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


class NaiveBayes:
    def __init__(self):
        self.test_loaded = False
        self.train_loaded = False

        self.posTestReviewsList = None
        self.negTestReviewsList = None
        self.probs = None
        self.zeroV = None
        self.emptyPos = None
        self.emptyNeg = None
        self.testDirPath = None
        self.folderpath = None
        self.pListLeng = None
        self.nListLeng = None


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

        self.load_train_folder()

        if self.folderpath is None:
            print("A training folder was not selected!")
            return

        posList, negList = nb.createArrayList(self.folderpath)
        print("made the lists")
        # lager dictionaries med antall reviews disse ordene forekommer i (ut av de positive/negative)
        negWordsDict = nb.addWords(negList)
        posWordsDict = nb.addWords(posList)
        allWords = Counter(negWordsDict) + Counter(posWordsDict)
        print("made the dicts")

        self.pListLeng = len(posList)
        self.nListLeng = len(negList)
        self.probs, self.zeroV, self.emptyPos, self.emptyNeg = nb.preProb(posWordsDict, self.pListLeng,
                                                      negWordsDict, self.nListLeng, allWords)

        self.train_loaded = True

    def saveData(self):
        """Saves model for quicker loading later"""
        if self.is_not_loaded():
            self.print_load_model()
            return
            
        values = {"probs": self.probs,
                  "zeroV": self.zeroV,
                  "emptyPos": self.emptyPos,
                  "emptyNeg": self.emptyNeg}

        with open(os.path.join(__location__, "preset_model.json"), "w") as outfile:
            json.dump(values, outfile)

    def load_data_from_file(self):
        """Loads a already generated model from loadData"""
        
        
        with open(os.path.join(__location__, "preset_model.json"), "r") as data:
            j_data = json.load(data)

            self.probs = j_data.get("probs", None)
            self.zeroV = j_data.get("zeroV", None)
            self.emptyPos = j_data.get("emptyPos", None)
            self.emptyNeg = j_data.get("emptyNeg", None)

        self.train_loaded = True

    def load_test_folder(self):
        """Loads folder with Test data"""
        print("choose your 'test' folder")
        tkinter.Tk().withdraw()
        self.test_loaded = True
        self.testDirPath = filedialog.askdirectory()

    def load_train_folder(self):
        """Loads folder with training data"""
        print("choose your 'train' folder")
        tkinter.Tk().withdraw()
        self.train_loaded = True
        self.folderpath = filedialog.askdirectory()

    def score(self):
        """
        Goes through every review in the test folder and attempts to classify it. 
        Then checks if the classification was right or not and updates the score 
        accordingly. Finally displays the score.
        """
        print("Select test folder")
        self.load_test_folder()
        self.set_review_list()
        print("Scoring... This may take a minute")
        if self.is_not_loaded():
            self.print_load_model()
            return

        tp = 0
        tn = 0
        #All positive reviews
        pos_c = len(self.posTestReviewsList)
        #All negative reviews
        neg_c = len(self.negTestReviewsList)
        total = pos_c + neg_c

        #Applies formula to each word in pos test directory, counts all positives (True positives)
        for rev in self.posTestReviewsList:
            neg, pos = nb.getProbs(rev, self.probs, self.zeroV, self.emptyPos, self.emptyNeg)
            if pos > neg:
                tp += 1

        #Applies formula to each word in neg test directory, counts all negatives (True negatives)
        for rev in self.negTestReviewsList:
            neg, pos = nb.getProbs(rev, self.probs, self.zeroV, self.emptyPos, self.emptyNeg)
            if pos < neg:
                tn += 1
        

        accuracy = (tp+tn)/total
        print(f"Accuracy {accuracy:.2%}")

        fp = pos_c - tp
        precision = tp / (tp+fp)
        print(f"Precision {precision:.2%}")

        fn = neg_c - tn
        recall = tp / (tp+fn)
        print(f"Recall {recall:.2%}")



    def is_not_loaded(self):
        """Check to avoid nullpointers"""
        return (self.probs is None or self.zeroV is None
                or self.emptyPos is None or self.emptyNeg is None
                or self.testDirPath is None)

    def print_load_model(self):
        """Message sent if model is not generated or imported before use0"""
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("============================================================")
        print("|Generate or import model before running any other command!|")
        print("============================================================")
        print()

    def classify(self, review=None):
        """
        attempts to classify a review submited by a user and prints if 
        it is posive or negative
        """

        if self.is_not_loaded():
            self.print_load_model()
            return
        if review is None:
            review = input("Give review to classify:")
        review_list = np.array(review.split())
        neg, pos = nb.getProbs(review_list, self.probs, self.zeroV, self.emptyPos, self.emptyNeg)
        if neg > pos:
            print("Your review is negative")
        else:
            print("Your review is positive")
