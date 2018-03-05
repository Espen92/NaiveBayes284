#%%
import jupyter
import numpy as np
import os

#%%


def load_files(path):
    """Loads files from given path, each file gets the class based on
    folder its stored in"""
    X = []
    y = []
    classes = []
    for file in os.listdir(path):
        fp = os.path.join(path, file)
        if os.path.isdir(fp):
            classes.append((file, fp))

    feat_num = 0
    for feature, path in classes:
        for file in os.listdir(path):
            with open(f"{path}/{file}", "r", encoding='utf8') as data:
                X.append(data.read().lower())
            y.append(feat_num)
        feat_num += 1
        # make pos 1 og neg 0 class stuff in array
    np_X = np.array(X)
    np_y = np.array(y)
    return np_X, np_y


#%%
train_path = os.path.abspath(
    "C:/Users/tagp/OneDrive/Dokumenter/Info 284/Group_Assignments_export/Data/train/train")

X_train, y_train = load_files(train_path)

#%%
X_train = [doc.replace("<br />", " ") for doc in X_train]

#%%
print("Samples per class (training): {}".format(np.bincount(y_train)))

#%%
X_test, y_test = load_files(
    "C:/Users/tagp/OneDrive/Dokumenter/Info 284/Group_Assignments_export/Data/test/test")

X_test = [doc.replace("<br />", " ") for doc in X_test]

#%%

from string import punctuation
table = str.maketrans('', '', punctuation)
res = [s.translate(table).split() for s in X_test]
print(res[0])

#%%
from collections import Counter
for sentence in res[:10]:
    c = Counter()
    c.update(sentence)
    print(c)
