

#%%
import jupyter
import NaiveBayesFunctions as nb
from collections import Counter


neg = "..\\Data\\train\\neg\\"
pos = "..\\Data\\train\\pos\\"
negativeData = nb.getTrainData(neg)
positiveData = nb.getTrainData(pos)

#%%
# lager en liste av de positive og en av de negative
posList = nb.createArrayList(positiveData, pos)
negList = nb.createArrayList(negativeData, neg)

# lager dictionaries med antall reviews disse ordene forekommer i (ut av de positive/negative)
negWordsDict = nb.addWords(negList)
posWordsDict = nb.addWords(posList)
allWords = Counter(negWordsDict) + Counter(posWordsDict)


#%%
# test
myTestReview = ["I", "liked", "it", "okay",
                "but", "I", "have", "seen", "better"]

probOfGood = nb.probOfPositive(
    myTestReview, posWordsDict, posList, negList, negWordsDict, allWords)
probOfBad = nb.probOfNegative(
    myTestReview, posWordsDict, posList, negList, negWordsDict, allWords)
print("Probability of review being good: ", probOfGood, "\n", "Probability of review being bad: ",
      probOfBad, "\n" "sum of probabilities: ", (probOfBad+probOfGood))
