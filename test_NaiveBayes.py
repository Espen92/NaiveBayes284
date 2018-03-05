import NaiveBayesFunctions as nb
import unittest
import numpy as np
from collections import Counter


class TestNaiveBayes(unittest.TestCase):

    def setUp(self):
        self.review1 = np.genfromtxt(
            ["This is one review"], case_sensitive='lower', dtype=str)
        self.review2 = np.genfromtxt(
            ["And this is another one"], case_sensitive='lower', dtype=str)
        self.review3 = np.genfromtxt(
            ["Pretty shitty movie btw"], case_sensitive='lower', dtype=str)
        self.review4 = np.genfromtxt(
            ["hey"], case_sensitive='lower', dtype=str)
        self.reviews = [self.review1, self.review2, self.review3, self.review4]
        self.allWords = nb.addWords(self.reviews)
        self.posList = [self.review1, self.review2]
        self.negList = [self.review3, self.review4]
        self.x = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.posWords = nb.addWords(self.posList)
        self.negWords = nb.addWords(self.negList)

    def test_addWords(self):
        testDict = nb.addWords(self.reviews)
        self.assertEqual(testDict["one"], 2)

    def test_prob(self):

        p = nb.prob(["I like this one"], self.posWords, self.x, self.allWords)
        p2 = nb.prob(["I like this one"], self.negWords, self.x, self.allWords)
        proPos = p/(p+p2)
        proNeg = p2/(p+p2)
        self.assertEqual((proPos+proNeg), 1)

    def test_probOfPos(self):
        proPos = nb.probOfPositive(
            ["s is"], self.posWords, self.x, self.x, self.negWords, self.allWords)
        proNeg = nb.probOfNegative(
            ["s is"], self.posWords, self.x, self.x, self.negWords, self.allWords)
        print(proPos, proNeg)


if __name__ == '__main__':
    unittest.main()
