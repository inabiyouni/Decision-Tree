class createNode():
    def __init__(self,):# id1, id2, id3, id4):
        self._label = ""
        #self._id = ""
        #self._lftChldID = ""
        #self._rghtChldID = ""
        self._leftChld = 0
        self._rghtChld = 0
        self._test_cond = 0
        self._attrNum = -1
        #self._id = "%d_%d_%d_%d_d%" %(id1, id2, id3, id4[0], id4[1])
    def distr(self, inst, v):
        dataSize = inst.shape
        numOfPnts = dataSize[0]
        subInst = np.matrix()
        for i in range(0,numOfPnts):
            if inst[i, self._test_cond] == v: np.append(subInst, inst[i,:], axis=0)
        return subInst
    #def setLftChldID(self, chldName):
    #    self._lftChldID = chldName
    #def setRghtChldID(self, chldName):
    #    self._rghtChldID = chldName
    def setLftChld(self, child):
        self._lftChld = child
    def setRghtChld(self, child):
        self._rghtChld = child
    def getLftChld(self):
        return self._lftChld
    def getRghtChld(self):
        return self._rghtChld
    def setTestCond(self, testCond):
        self._test_cond = testCond
    def getTestCond(self):
        return self._test_cond
    def setLabel(self, label):
        self._label = label
    def getLabel(self):
        return self._label
    def setAttrNum(self, attrNum):
        self._attrNum = attrNum
    def getAttrNum(self):
        return self._attrNum

    #def getID(self):
    #    return self._id