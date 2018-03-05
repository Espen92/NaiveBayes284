

#%%
import jupyter
import NaiveBayesFunctions as nb
from collections import Counter
import math
import pathlib


neg = "..\\Data\\train\\neg\\"
pos = "..\\Data\\train\\pos\\"
negativeData = nb.getTrainData(neg)
positiveData = nb.getTrainData(pos)

# lager en liste av de positive og en av de negative
posList = nb.createArrayList(positiveData, pos)
negList = nb.createArrayList(negativeData, neg)

# lager dictionaries med antall reviews disse ordene forekommer i (ut av de positive/negative)
negWordsDict = nb.addWords(negList)
posWordsDict = nb.addWords(posList)
allWords = Counter(negWordsDict) + Counter(posWordsDict)


testNeg = "..\\Data\\test\\neg\\"
testPos = "..\\Data\\test\\pos\\"

posTestReviewsList = nb.createArrayList(nb.getTrainData(testPos), testPos)
negTestReviewsList = nb.createArrayList(nb.getTrainData(testNeg), testNeg)

#%%
gotItRight = 0
counter = 0
pListLeng = len(posList)
nListLeng = len(negList)
for rev in posTestReviewsList:
    neg, pos = nb.getProbs(rev, posWordsDict, pListLeng,
                           nListLeng, negWordsDict, allWords)
    print(neg, pos, (neg+pos))


#%%
# test
myTestReview = ["I", "liked", "it", "it", "was", "nice"]

probOfGood = nb.probOfPositive(
    myTestReview, posWordsDict, len(posList), len(negList), negWordsDict, allWords)
probOfBad = nb.probOfNegative(
    myTestReview, posWordsDict, len(posList), len(negList), negWordsDict, allWords)
print("Probability of review being good: ", probOfGood, "\n", "Probability of review being bad: ",
      probOfBad, "\n" "sum of probabilities: ", (probOfBad+probOfGood))
