import NaiveBayesFunctions as nb
import unittest
import numpy as np


class TestNaiveBayes(unittest.TestCase):

    def setUp(self):
        self.review1 = np.genfromtxt(
            ["This is one review"], case_sensitive='lower', dtype=str)
        self.review2 = np.genfromtxt(
            ["And this is another one"], case_sensitive='lower', dtype=str)
        self.review3 = np.genfromtxt(
            ["Pretty shitty movie btw"], case_sensitive='lower', dtype=str)
        self.review4 = np.genfromtxt(
            ["Needs more JPEG"], case_sensitive='lower', dtype=str)
        self.reviews = [self.review1, self.review2, self.review3, self.review4]

    def test_addWords(self):
        testDict = nb.addWords(self.reviews)
        self.assertEqual(testDict["one"], 2)


if __name__ == '__main__':
    unittest.main()
