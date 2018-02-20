import xml.etree.cElementTree as ET


class saveTree():
    def __init__(self, r):
        self._rrot = r

    root = ET.Element("Node", id="name")
    doc = ET.SubElement(root, "data")
    lftChld = ET.SubElement(root, "Node", name="leftChild")
    rghtChld = ET.SubElement(root, "Node", name="rightChild")

    ET.SubElement(doc, "test_cond").text = ""
    ET.SubElement(doc, "label").text = ""

    tree = ET.ElementTree(root)
    tree.write("filename.xml")

    #tree = ElementTree.ElementTree()
    #root = ElementTree.Element("Node")
    #root.text
    #a = ElementTree.Element("a")
    #a.text = "1"
    #root.append(a)
    #ree._setroot(root)
    #tree.write("sample.xml")
