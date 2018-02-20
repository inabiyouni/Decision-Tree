import xml.etree.cElementTree as ET
from makeTree import makeTree
from readData import readData
import numpy as np
import sys

def estimateData(data, root):
    if root.getLabel() != "":
        estClass = root.getLabel()
        return estClass
    testCond = float(root.getTestCond())
    atrbNum = data[int(root.getAttrNum())]
    if atrbNum <= testCond: return estimateData(data, root.getLftChld())
    else: return estimateData(data, root.getRghtChld())

def TreeResult (data, root):
    r = []
    for inst in data:
        estClass = estimateData(inst, root)
        realClass = inst[-1]
        crrctEst = (realClass == int(estClass[:-2]))
        r.append(crrctEst)
    return r

#main body of the program for loading data, tree and
# estimating classes of the test data
args = iter(sys.argv)
next(args)
mdlName = ""
inputFileTr = ""
inputClassesTr = ""
inputFileTs = ""
inputClassesTs = ""
for item in args:
    if item == "-m":
        mdlName = next(args)
    elif item == "-itr1":
        inputFileTr = next(args)
    elif item == "-itr2":
        inputClassesTr = next(args)
    elif item == "-its1":
        inputFileTs = next(args)
    elif item == "-its2":
        inputClassesTs = next(args)

if inputFileTr.lower() == "" or inputClassesTr == "" or (mdlName.lower() != "test"  and mdlName.lower() != "train"):# or inputFileTs.lower() == "" or inputClassesTs.lower() == "":
    print("You have NOT entered one of the required inputs!")
    sys.exit()

#inputFileTr = "X_train.txt"
#inputClassesTr = "y_train.txt"
#inputFileTs = "X_test.txt"
#inputClassesTs = "y_test.txt"

print("\nLoading saved tree ...")
tree = ET.ElementTree(file="trained_Tree.xml")
xmlRoot = tree.getroot()
root = makeTree(xmlRoot)
print("\nReading 1 set of data ...")
clases = readData(inputClassesTr)
data1 = readData(inputFileTr)
data1 = np.append(data1, clases, axis=1)

if inputClassesTs != "":
    print("\nReading 2 set of data ...")
    clases = readData(inputClassesTs)
    data2 = readData(inputFileTs)
    data2 = np.append(data2, clases, axis=1)

data = np.append(data1, data2, axis=0) if inputClassesTs != "" else data1

randIndx = np.load('invtRandData.npy') if (mdlName.lower() == "test") else np.load('randData.npy')

print("Estimating classes and calculating accuracy ...")
result = TreeResult (data[randIndx, :], root)
crrts = sum(result)
print("Accuracy of the model is = %0.2f" %(crrts / float(len(result))))