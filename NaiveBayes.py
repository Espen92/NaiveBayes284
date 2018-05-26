import os
import json
from pathlib import Path
import tkinter
from tkinter import filedialog
from string import punctuation
from collections import Counter

import numpy as np

import NaiveBayesFunctions as nb



_location = Path(__file__).resolve().parent


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
        if not self.train_loaded:
            print("Training data not loaded")
            return

        values = {"probs": self.probs,
                  "zeroV": self.zeroV,
                  "emptyPos": self.emptyPos,
                  "emptyNeg": self.emptyNeg}

        with Path(_location.joinpath("preset_model.json")).open() as outfile:
            json.dump(values, outfile)

    def load_data_from_file(self):
        """Loads a already generated model from loadData"""
        
        
        with Path(_location.joinpath("preset_model.json")).open() as data:

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
        self.set_review_list()

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
        #print("Select test folder")
        # self.load_test_folder()
        if not self.test_loaded or not self.train_loaded:
            print("Test or training data not loaded")
            return

        # self.set_review_list()
        print("Scoring... This may take a minute")
        if self.is_not_loaded():
            self.print_load_model()
            return

        tp = 0
        tn = 0
        # All positive reviews
        pos_c = len(self.posTestReviewsList)
        # All negative reviews
        neg_c = len(self.negTestReviewsList)
        total = pos_c + neg_c

        # Applies formula to each word in pos test directory, counts all positives (True positives)
        for rev in self.posTestReviewsList:
            neg, pos = nb.getProbs(
                rev, self.probs, self.zeroV, self.emptyPos, self.emptyNeg)
            if pos > neg:
                tp += 1

        # Applies formula to each word in neg test directory, counts all negatives (True negatives)
        for rev in self.negTestReviewsList:
            neg, pos = nb.getProbs(
                rev, self.probs, self.zeroV, self.emptyPos, self.emptyNeg)
            if pos < neg:
                tn += 1

        fp = pos_c - tp
        fn = neg_c - tn
        accuracy = (tp+tn)/total
        print(f"Accuracy {accuracy:.2%}")

        precision = tp / (tp+fp)
        print(f"Precision {precision:.2%}")

        recall = tp / (tp+fn)
        print(f"Recall {recall:.2%}")

        print(f"""
        \rTrue Positives : {tp}
        \rTrue Negatives : {tn}
        \rFalse Positives: {fp}
        \rFalse Negatives: {fn}""")

    def is_not_loaded(self):
        """Check to avoid nullpointers"""
        return (self.probs is None or self.zeroV is None
                or self.emptyPos is None or self.emptyNeg is None)


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

        table = str.maketrans('', '', punctuation)
        review = review.lower()
        cleanText = review.translate(table)
        review_list = np.array(cleanText.split())
        neg, pos = nb.getProbs(review_list, self.probs, self.zeroV, self.emptyPos, self.emptyNeg)

        if neg > pos:
            print("Your review is negative")
        else:
            print("Your review is positive")
