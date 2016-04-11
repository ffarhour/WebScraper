from lxml import html
from lxml import etree
import requests
#from urlparse import urlparse #to parse root urls


global g_xml_namespace
g_xml_namespace = "http://www.w3.org/XML/1998/namespace"

#function to save to file
def saveToFile(xml, filename):
	f = open(filename+".xml", 'w')
	f.write(xml)
	f.close()

def getHtml(url):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	tree.make_links_absolute(url,resolve_base_href=True)
	return tree

#fetch html page
url = raw_input("Please enter the url to the site: \n") or "http://stackoverflow.com/questions/138175/dotnetnuke-vulnerabilities"
#parse the domain url of the website
#parsed_uri = urlparse(url)
#g_domain_path = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
tree = getHtml(url)


# create basic POS XML structure
#
TEI = etree.Element('TEI')
TEI.set('xmlns','http://www.tei-c.org/ns/1.0')
##
teiHeader = etree.SubElement(TEI,'teiHeader')
###
fileDesc = etree.SubElement(teiHeader,'fileDesc')
####
titleStmt = etree.SubElement(fileDesc, 'titleStmt')
#####
title = etree.SubElement(titleStmt,'title')
title.text = tree.xpath(".//h1[@itemprop='name']//a[@class='question-hyperlink']/text()")[0]
#####
author = etree.SubElement(titleStmt,'author')
author.text = tree.xpath(".//td[@class='post-signature owner']//div[@class='user-details']/a/text()")[0]
####
sourceDesc = etree.SubElement(fileDesc,'sourceDesc')
#####
p = etree.SubElement(sourceDesc,'p')
p.text = " Pulled from StackOverflow: "+url
###
listPerson = etree.SubElement(teiHeader,'listPerson')
####
person = etree.SubElement(listPerson,'person')
#person.set("xml:id",tree.xpath(".//td[@class='post-signature owner']//div[@class='user-details']/a/text()")[0])
person.attrib[etree.QName(g_xml_namespace,"id")]=tree.xpath(".//td[@class='post-signature owner']//div[@class='user-details']/a/text()")[0]
person.set('url',tree.xpath(".//td[@class='post-signature owner']//div[@class='user-details']/a/@href")[0])
#####
signatureContent = etree.SubElement(person,'signatureContent')
######
p = etree.SubElement(signatureContent,'p')
p.text = "Reputation: "
#######
num = etree.SubElement(p,'num')
num.text = tree.xpath(".//td[@class='post-signature owner']//span[@class='reputation-score']/text()")[0]
num.tail = "Number of Gold Badges: "
num = etree.SubElement(p,'num')
num.text = tree.xpath(".//td[@class='post-signature owner']//span[@class='badgecount']/text()")[0]
num.tail = "Number of Silver Badges: "
num = etree.SubElement(p,'num')
num.text = tree.xpath(".//td[@class='post-signature owner']//span[@class='badgecount']/text()")[1]
num.tail = "Number of Bronze Badges: "
num = etree.SubElement(p,'num')
num.text = tree.xpath(".//td[@class='post-signature owner']//span[@class='badgecount']/text()")[2]
####
answers_person = tree.xpath(".//div[@id='answers']//div[@class='user-details']")

for i in answers_person:
	person = etree.SubElement(listPerson,'person')
	person.attrib[etree.QName(g_xml_namespace,"id")] = i.xpath(".//a/text()")[0]
	person.attrib["url"] = i.xpath(".//a/@href")[0]



# pretty string
s = etree.tostring(TEI,pretty_print=True)
saveToFile(s,"test")
