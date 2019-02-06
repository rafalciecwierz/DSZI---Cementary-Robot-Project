import csv
from sklearn import tree

X = []
Y = []

with open('decisiontreeTrainingSet.csv', newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=';')
    for row in data:
        Y.append(row.pop())
        X.append(row)

X.pop(0)
Y.pop(0)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)

def getPriority(tomb):
    return int(clf.predict([tomb]))
