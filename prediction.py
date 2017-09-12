
import readFile as file;
import random
import operator
import sys,os
import chardet
reload(sys)
sys.setdefaultencoding("utf-8")
from sklearn.datasets import load_boston
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.tree import export_graphviz
from sklearn import tree

# training
# sampleNumber = 10
# dataPath = "../data/traindata.txt";
# dataPath = "../data/training.txt"
dataPath = "../data/shakeTraining.txt"
header,datas = file.readfiles(dataPath, True, "utf-8","\t")
print 'header: '+str(header)
# to tune the features: [0,9] for statistical indices;
# [10, 22] for unweighted motifs; [23, 79] for weighted motifs
# and [80, 81] are main-category and sub-category
# featureIndex = range(0, 10)
# featureIndex = [6]
# featureIndex = range(10, 23)
# featureIndex = range(23, 80)
# featureIndex = range(10, 80)
# featureIndex.extend(range(0, 10))
# featureIndex.append(6)
featureIndex = range(0,len(header)-1)
ommitFeatureIndex= [] #[1,3,4,6,7,11]
# len(header)-1: 5 categories; len(header)-2: len(header)-2
targetIndex = len(header)-1

trainData=[]
trainResult=[]

for p in datas:
    row = []
    for f in featureIndex:
        if f not in ommitFeatureIndex:
            row.append(float(p[f]))
    trainData.append(row)
    trainResult.append(p[targetIndex])

trainData = np.array(trainData)
trainResult = np.array(trainResult)

# testing
# dataPath = "../data/testdata.txt";
dataPath = "../data/shakeTesting.txt"
header,datas = file.readfiles(dataPath, True, "utf-8","\t")

testData=[]
testResult=[]

for p in datas:
    row = []
    for f in featureIndex:
        if f not in ommitFeatureIndex:
            row.append(float(p[f]))
    testData.append(row)
    testResult.append(p[targetIndex])

testData = np.array(testData)
testResult = np.array(testResult)

clf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
                             max_depth=2, max_features='auto', max_leaf_nodes=None,
                             min_impurity_split=0,
                             min_samples_leaf=1, min_samples_split=2,
                             min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
                             oob_score=False, random_state=0, verbose=0, warm_start=False)
clf.fit(trainData, trainResult)
prediction = clf.predict(testData)
count = 0
for i in range(0,len(testResult)):
    if prediction[i]==testResult[i]:
        count=count+1
print str(len(testResult)) + "\t" + str(count) + "\t" + str(count*1.0/len(testResult))

