import numpy as np
import copy
from dataInfo import dataInfo
from createNode import createNode
import xml.etree.cElementTree as ET
from readData import readData
import sys

def getDistOfPnts(subMat):
    dict = {}
    for key in subMat[:,-1]:
        if key in dict:
            dict[key] += 1
        else:
            dict[key] = 1
    return dict

def calGain(dict1, dict2, mdlName):
    sumFor1 = 0.0
    sumFor2 = 0.0
    n1 = 0.0
    n2 = 0.0
    for key in dict1.keys():
        n1 += dict1[key]
        n2 += dict2[key]
        if mdlName == 'gini':
            sumFor1 += (dict1[key]) ** 2
            sumFor2 += (dict2[key]) ** 2
        elif mdlName == 'information gain':
            if dict1[key] != 0.0: sumFor1 += (dict1[key]) * np.log2(dict1[key])
            if dict2[key] != 0.0: sumFor2 += (dict2[key]) * np.log2(dict2[key])
    if mdlName == 'gini':
        if n1 != 0.0:sumFor1 = 1 - sumFor1 / (n1 ** 2)
        if n2 != 0.0: sumFor2 = 1 - sumFor2 / (n2 ** 2)
    elif mdlName == 'information gain':
        if n1 != 0.0:sumFor1 = np.log2(n1) - sumFor1 / n1
        if n2 != 0.0: sumFor2 = np.log2(n2) - sumFor2 / n2
    try:
        r = n1/(n1+n2)* sumFor1 + n2 / (n1 + n2)* sumFor2
    except Exception as error:
        print('Caught this error: ' + repr(error))
    return n1, n2, r

def findTresh(firstPnt, secondPnt, prntGain, subMat, n1, n2, mdlName):
    chldGain = prntGain
    bestSndPnt = {}
    bestFrstPnt = {}
    bestInd = 0

    for c in subMat[:, -1]:
        firstPnt[c] +=1
        secondPnt[c] -= 1
        n1 += 1
        n2 -= 1
        _, _, gain = calGain(firstPnt, secondPnt, mdlName)
        if gain < chldGain :
            chldGain = gain
            bestFrstPnt = copy.copy(firstPnt)
            bestSndPnt = copy.copy(secondPnt)
            bestInd = int(n1)
        #gain = np.append(gain, [calGain(firstPnt, secondPnt, n1, n2)], axis=0)

    splitGn = prntGain - chldGain
    return splitGn, bestFrstPnt, bestSndPnt, bestInd

def find_best_split(inst, mdlName):
    secondPnt = inst.clsDist
    firstPnt = {}
    for key in secondPnt.keys():
        firstPnt[key] = 0
    [n1, n2, prntGain] = calGain(firstPnt, secondPnt, mdlName)
    maxSpltGn = -1
    maxGnInd = -1

    for i in range(0,len(inst.data[0,:])-1):
        numbAttr = inst.data[:,i].astype(float)
        #if np.isnan(inst.indices[0,i]):
        ind = (numbAttr).argsort()
        inst.indices[:,i] = ind
        #else:
        #    ind = range(0,inst.data[:,0].size)
        subMat = np.array([numbAttr[ind], inst.data[ind, - 1]]).transpose()
        #[firstPnt, secondPnt, n1, n2] = getDistOfPnts(subMat)
        [splitGn, _, _, _] = findTresh(copy.copy(firstPnt), copy.copy(secondPnt), prntGain, subMat, n1, n2, mdlName)
        if splitGn > maxSpltGn:
            maxSpltGn = splitGn
            maxGnInd = i
    if maxSpltGn == 0:
        print("No progress error")
    numbAttr = inst.data[:, maxGnInd].astype(float).transpose()
    ind = inst.indices[:, maxGnInd].astype(int)
    subMat = np.array([numbAttr[ind], inst.data[ind, - 1]]).transpose()
    [splitGn, bestFrstPnt, bestSndPnt, bestInd] = findTresh(copy.copy(firstPnt), copy.copy(secondPnt), prntGain, subMat, n1, n2, mdlName)
    tresh = (numbAttr[ind[bestInd-1]]+ numbAttr[ind[bestInd]]) / 2.0
    sub1 = inst.data[ind[0:bestInd], :]
    sub2 = inst.data[ind[bestInd:], :]
    #indicesMat = (inst.indices[:,:-1])
    #indicesMat = indicesMat.flatten('F')
    #indicesMat = np.reshape(indicesMat,)
    #maskMat = inst.indices[:,maxGnInd] < bestInd
    #vecInd1 = indicesMat[maskMat]
    #vecInd2 = indicesMat[np.invert(maskMat)]
    #indices1 = np.reshape(vecInd1, (bestInd, 3), order='F')
    #indices2 = np.reshape(vecInd2, (10 - bestInd, 3), order='F')
    #indices1 = inst.indices[maskMat,:]
    #indices2 = inst.indices[np.invert(maskMat),:]
    #print(inst.indices, '\n', indices1, '\n', indices2)
    node1 = dataInfo(sub1, bestFrstPnt, np.zeros(shape=(sub1).shape))
    node2 = dataInfo(sub2, bestSndPnt, np.zeros(shape=(sub2).shape))
    return node1, node2, tresh, maxGnInd

#def find_best_split(inst, attr):
#    dataSize = inst.shape
#    numOfClm = dataSize[1]
#    numOfRow = dataSize[0]
#    [clsDist1, clsDist2, splitGn, sub1, sub2, thresh] = calImpurity(inst, attr)
#    while (splitGn < 0 and attr[0] < numOfClm-1):
#        attr[0] += 1
#        attr[1] = 0
#        [clsDist1, clsDist2, splitGn, sub1, sub2, thresh] = calImpurity(inst, attr)
#    if splitGn <0: print("ERROR!")
#    return clsDist1, clsDist2, thresh, sub1, sub2,

def stopping_cond(inst, mdlName, epsl):
    try:
        _, _, gain = calGain(inst.clsDist, inst.clsDist, mdlName)
    except Exception as error:
        _, _, gain = calGain(inst.clsDist, inst.clsDist, mdlName)
    try:
        a1 = (inst.data[:,0].size) * inst.data[0,:-1]
    except Exception as error:
        print('Caught this error: ' + repr(error))
    a2 = np.sum(inst.data[:, :-1], axis=0)
    if gain < epsl or  np.array_equal(a1, a2) :
        return True
    return False

def Classify(clsDist):
    mainClass = 0
    mainKey = 0
    for key in clsDist:
        if clsDist[key] > mainClass: mainKey = key
    return mainKey

def TreeGrowth (inst, level, mdlName, root = None):
    level += 1
    if root == None:
        inst.indices = np.zeros(shape=(inst.data).shape)
        #inst.sorted = np.zeros(shape=(inst.data[0,:]).shape)
        inst.indices[:] = np.nan
        inst.clsDist = getDistOfPnts(inst.data)
        root = ET.Element("Node", name="root")
    if stopping_cond(inst, mdlName, 0.001) == True:
        #leaf = createNode(clsDist)
        #leaf.setLabel()
        label = Classify(inst.clsDist)
        data = ET.SubElement(root, "data")
        ET.SubElement(data, "test_cond").text = ""
        ET.SubElement(data, "label").text = repr(label)
        ET.SubElement(data, "attrNum").text = ""
        #print(inst.data,'\n\n')
        return 0#leaf
    else:
        #key = iter(clsDist)
        #root = createNode(level, clsDist[next(key)], clsDist[next(key)], inst.shape)
        [node1, node2, v, maxGnInd]= find_best_split(inst, mdlName)
        data = ET.SubElement(root, "data")
        ET.SubElement(data, "test_cond").text = repr(v)
        ET.SubElement(data, "label").text = ""
        ET.SubElement(data, "attrNum").text = repr(maxGnInd)
        lftChld = ET.SubElement(root, "Node", name="leftChild")
        child = TreeGrowth(node1, level, mdlName, lftChld)
        #root.setLftChld(child.getID)
        #root.addTestCond(v)
        rghtChld = ET.SubElement(root, "Node", name="rightChild")
        child = TreeGrowth(node2, level, mdlName, rghtChld)
        #root.setRghtChld(child.getID)
        #for v in V:
        #    subInst = distr(inst, v) #(e I root.test..cond(e) = v and e EE}.
        #    child= TreeGrowth(subInst, attr)
        #    root.addEdge(v, child)
    return root

#main body of the program for loading data and
# running a recursive tree function to learn from data
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

if inputFileTr.lower() == "" or inputClassesTr == "" or (mdlName.lower() != "gini"  and mdlName.lower() != "information gain"):#or inputFileTs.lower() == "" or inputClassesTs.lower() == "" or
    print("You have NOT entered one of the required inputs!")
    sys.exit()

#mdlName = "information gain"
#inputFileTr = "X_iris.txt"
#inputClassesTr = "y_iris.txt"
#inputFileTs = "X_test.txt"
#inputClassesTs = "y_test.txt"

print("\nReading 1 set of data ...")
clases = readData(inputClassesTr)
data1 = readData(inputFileTr)
data1 = np.append(data1, clases, axis=1)

if inputClassesTs != "":
    print("\nReading 2 set of data ...")
    clases = readData(inputClassesTs)
    data2 = readData(inputFileTs)
    data2 = np.append(data2, clases, axis=1)

data = np.append(data1, data2, axis=0) if (inputClassesTs != "") else data1

#sh = instances.shape
#data = np.empty((sh[0], sh[1]+1), float)
#print(data.shape)
#data[:,:-1] = instances
#data[:,-1] = clases
#data = np.array([[1, 1, 125, "No"],
#                [0, 2, 100, "Yes"],
#                [0, 1, 70, "No"],
#                [1, 2, 120, "No"],
#                [0, 3, 95, "Yes"],
#                [0, 2, 60, "No"],
#                [1, 3, 220, "No"],
#                [0, 1, 85, "Yes"],
#                [0, 2, 75, "No"],
#                [0, 1, 90, "Yes"]])

print("\nTraining a tree model ...")
arraySize = int(data[:,0].size )
randIndx = np.random.choice([True, False], arraySize)#[bool(random.getrandbits(1)) for i in range(arraySize)]
invIndx = [not i for i in randIndx]
np.save( 'randData' , randIndx)
np.save( 'invtRandData' , invIndx)
inst = dataInfo(data[randIndx, :])
root = TreeGrowth (inst, 0, mdlName.lower())

tree = ET.ElementTree(root)
tree.write("trained_Tree.xml")
print("\nThe tree model has been trained,\nYou can look at it in a file named \"trained_Tree.xml\"\nwhich is created inside your project folder")
#saveTree(root)