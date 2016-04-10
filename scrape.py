from lxml import html
from lxml import etree
#from xml.etree.ElementTree import Element, SubElement, Comment, tostring
#from elementtree.ElementTree import Element, SubElement,tostring
#from xml.etree import ElementTree as ET
import requests

def saveToFile(xml, filename):
	f = open(filename+".xml", 'w')
	f.write(xml)
	f.close()



page = requests.get('http://stackoverflow.com/questions/138175/dotnetnuke-vulnerabilities')
tree = html.fromstring(page.content)
content=tree.xpath('//title/text()')
print(content)



# create basic POS XML structure
TEI = etree.Element('TEI')
TEI.set('xmlns','http://www.tei-c.org/ns/1.0')
teiHeader = etree.SubElement(TEI,'teiHeader')
fileDesc = etree.SubElement(teiHeader,'fileDesc')
titleStmt = etree.SubElement(fileDesc, 'titleStmt')
title = etree.SubElement(titleStmt,'title')
title.text = content[0]
#author = etree.SubElement(titleStmt,tree.xpath(".//div[@class='user-details']/text()")[0])

# pretty string
s = etree.tostring(TEI,pretty_print=True)
saveToFile(s,"test")
