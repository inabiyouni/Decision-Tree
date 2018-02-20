import xml.etree.cElementTree as ET
from createNode import createNode

def makeTree (xmlRoot):
    #level += 1
    #if clsDist == None:
    #    clsDist = getDistOfPnts(inst)
    #    root = ET.Element("Node", name="root")
    data = xmlRoot[0]
    if data[1].text != None:
        leaf = createNode()
        leaf.setLabel(data[1].text)

        #ET.SubElement(root, "test_cond").text = ""
        #ET.SubElement(root, "label").text = label
        return leaf
    else:
        #key = iter(clsDist)
        root = createNode()
        #[clsDist1, clsDist2, v, sub1, sub2]= find_best_split(inst, clsDist, attr)
        #data = ET.SubElement(root, "data")
        #ET.SubElement(data, "test_cond").text = repr(v)
        #ET.SubElement(data, "label").text = ""
        #lftChld = ET.SubElement(root, "Node", name="leftChild")
        child = makeTree(xmlRoot[1])
        root.setLftChld(child)
        root.setTestCond(data[0].text)
        root.setAttrNum(data[2].text)
        #rghtChld = ET.SubElement(root, "Node", name="rightChild")
        child = makeTree(xmlRoot[2])
        root.setRghtChld(child)
        #for v in V:
        #    subInst = distr(inst, v) #(e I root.test..cond(e) = v and e EE}.
        #    child= TreeGrowth(subInst, attr)
        #    root.addEdge(v, child)
    return root