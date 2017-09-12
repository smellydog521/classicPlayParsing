from sklearn import preprocessing
import readFile as file;
import random
import operator
import sys
import chardet
reload(sys)
sys.setdefaultencoding("utf-8")
from sklearn.datasets import load_boston
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import matplotlib.pyplot as plt

sampleNumber = 10
# dataPath = "../data/traindata.txt";
dataPath = "../data/training3.txt"
# full.txt: with all training and testing data
# training3.txt: with (0, 10)+(23, 80)
header,datas = file.readfiles(dataPath, True, "utf-8","\t")
print header

# to tune the features: [0,9] for statistical indices;
# [10, 22] for unweighted motifs; [23, 79] for weighted motifs
# and [80, 81] are main-category and sub-category
# featureIndex = range(23, 80)
featureIndex = range(0,len(header)-2)
ommitFeatureIndex= [] #[1,3,4,6,7,11]
# ommitFeatureIndex= range(10,23)
# len(header)-1: 5 categories; len(header)-2: len(header)-2
targetIndex = len(header)-1

trainData=[]
trainResult=[]
categories=[]
le = preprocessing.LabelEncoder()

for p in datas:
    row = []
    for f in featureIndex:
        if f not in ommitFeatureIndex:
            row.append(float(p[f]))
    trainData.append(row)
    trainResult.append(p[targetIndex])
    if p[targetIndex] not in categories:
        categories.append(p[targetIndex])
tmpHeader=[]
for h in header:
    if header.index(h) not in ommitFeatureIndex:
        tmpHeader.append(h)
header=tmpHeader
trainData = np.array(trainData)
le.fit(categories)
trainResult = le.transform(trainResult)
print trainResult
rf = RandomForestRegressor()
rf.fit(trainData, trainResult)

importances = rf.feature_importances_
print importances
std = np.std([tree.feature_importances_ for tree in rf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]
print indices
# Print the feature ranking
print("Feature ranking:")

xticks = []
xindex = []
ximport = []
for f in range(trainData.shape[1]):
    if importances[f]>0:
        xindex.append(f)
        ximport.append(importances[indices[f]])
        xticks.append(header[indices[f]])
        print("%d. feature %d  %s (%f)" % (f + 1, indices[f] ,header[indices[f]], importances[indices[f]]))

xticks = np.array(xticks)

# Plot the feature importances of the forest
plt.figure()

font = {'size'   : 40}
plt.rc('font', **font)

print xindex,ximport

plt.title("Feature importances")
plt.bar(range(len(xindex)), ximport,
        color="r", align="center")
plt.xticks(range(len(xindex)), xticks, rotation='vertical',fontsize=15)  #, rotation='vertical'
plt.show()

print "Features sorted by their score:"
print sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), np.array(featureIndex)),
             reverse=True)





