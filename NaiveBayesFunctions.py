import os
import math

import numpy as np
from collections import Counter
from string import punctuation

def createArrayList(path):
    """
    Lager to lister med numpy arrays for alle ordene

    Keyword arguments:
    path -- directory som inneholder pos og neg mappen for filene

    returns:
    pos_list -- Liste med reviews splitta i numpy array for orda (Positive reviews)
    neg_list -- Liste med reviews splitta i numpy array for orda (Negative reviews)
    """
    pos_list = []
    neg_list = []
    neg = os.listdir(path+"\\neg\\")
    pos = os.listdir(path+"\\pos\\")
    table = str.maketrans('', '', punctuation)
    print(f"Loading: {path}")
    print(
        f"This set contains {len(neg)+len(pos)} files\nNow loading the set please wait...")
    for i, file_ in enumerate(neg):
        print(f"Loaded file {(i+1)/len(neg):.0%} from negative...", end="\r")
        with open(path+"\\neg\\"+file_, encoding='utf-8') as f:
            text = f.read().lower()
            cleanText = text.translate(table)
            wordsarray = np.array(cleanText.split())
            neg_list.append(wordsarray)

    for i, file_ in enumerate(pos):
        print(
            f"Loaded file {(i+1)/len(pos):.0%} from positive...", end="\r")
        with open(path+"\\pos\\"+file_, encoding='utf-8') as fi:
            text = fi.read().lower()
            cleanText = text.translate(table)
            wordsarray = np.array(cleanText.split())
            pos_list.append(wordsarray)
    print()
    print("Loading done")
    return pos_list, neg_list


# tar inn en liste av words arrays og returnerer en dictionary som inneholder
# hvert ord som finnes i noe array i den listen som keys. Disse har verdier
# som tilsvarer antall reviews som inneholder det ordet

def addWords(theList):
    """
    Tar inn en liste av ord nmp arrays og returnere en dictionary som inneholder
    hvert ord som finnes i noe array med ordet som key, og verdi som antall forekomster av ordet

    Keyword arguments:
    theList -- Listen med nmp arrays som inneholder ord (liste med reviews splitta i nmp arrays)

    returns:
    dic --  Dictionary hvor hvert ord er scora basert på frequency
    """
    dic = Counter()
    for eachReview in theList:
        tempDic = {}
        if (eachReview.shape == ()):
            eachReview = np.array([""])
        for everyWord in eachReview:
            if everyWord not in tempDic:
                tempDic[everyWord] = True
                if everyWord in dic:
                    dic[everyWord] += 1
                else:
                    dic[everyWord] = 1
    return dic


def preProb(poswordsDict, poslisLen, negwordsDict, neglisLen, allWords):
    print("")
    allWLeng = len(allWords)
    new_dict = {}
    emptyPosProb = math.log(0.5)
    emptyNegProb = math.log(0.5)
    for i, word in enumerate(allWords):
        print(f"Calculating... {(i+1)/len(allWords):.0%}", end="\r")
        x = (math.log((negwordsDict[word]+1)/(allWLeng+neglisLen)),
             math.log((poswordsDict[word]+1)/(allWLeng+poslisLen)),
             math.log(1-(negwordsDict[word]+1)/(allWLeng+neglisLen)),
             math.log(1-(poswordsDict[word]+1)/(allWLeng+poslisLen))
             )
        new_dict[word] = x
        emptyNegProb += x[2]
        emptyPosProb += x[3]
    firstTimeValue = (math.log(1/(allWLeng+neglisLen)),
                      math.log(1/(allWLeng+poslisLen)),
                      math.log(1-1/(allWLeng+neglisLen)), 
                      math.log(1-1/(allWLeng+poslisLen))
                      )

    return new_dict, firstTimeValue, emptyPosProb, emptyNegProb


def prob(review, probsDict, firstTimeValue, emptyPosProb, emptyNegProb):
    if review.shape != ():
        for word in review:
            if word not in probsDict:
                probsDict[word] = firstTimeValue
                emptyPosProb += firstTimeValue[1]
                emptyNegProb += firstTimeValue[0]
            else:
                wProbs = probsDict[word]
                emptyNegProb += (wProbs[0] - wProbs[2])
                emptyPosProb += (wProbs[1] - wProbs[3])

    return emptyPosProb, emptyNegProb


def getProbs(review, probs, zeroV, emptyPosProb, emptyNegProb):
    po, ne = prob(review, probs, zeroV, emptyPosProb, emptyNegProb)
    probOfPos = po/(po+ne)
    probOfNeg = ne/(po+ne)
    return probOfPos, probOfNeg
