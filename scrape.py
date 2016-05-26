from lxml import html
from lxml import etree
import requests
import os.path


global g_xml_namespace
g_xml_namespace = "http://www.w3.org/XML/1998/namespace"

class bcolors:
    """Used to implement ANSI colors without the need to remember the numbers.
    Does not contain any methods. Only contains variables.
    Usage: simply concatenate bcolors.<color> at the start of string to be printed,
        and bcolors.ENDC at the end of the string, to color the string with the
        specified color.
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#function to save to file
def saveToFile(xml, filename):
    #increment name no. if already exists
    n = 0
    while(os.path.isfile(filename + str(n) + ".xml")==True):
        n = n+1
    f = open(filename+str(n)+".xml", 'wb')
    f.write(xml)
    f.close()
    print("All done! Filename: "+ filename + str(n) + ".xml")

def getHtml(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    tree.make_links_absolute(url,resolve_base_href=True)
    return tree



##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
    # import re, htmlentitydefs
    # def fixup(m):
    #     text = m.group(0)
    #     if text[:2] == "&#":
    #         # character reference
    #         try:
    #             if text[:3] == "&#x":
    #                 return unichr(int(text[3:-1], 16))
    #             else:
    #                 return unichr(int(text[2:-1]))
    #         except ValueError:
    #             pass
    #     else:
    #         # named entity
    #         try:
    #             text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
    #         except KeyError:
    #             pass
    #     return text # leave as is
    # return re.sub("&#?\w+;", fixup, text)
    from html import unescape
    #h = HTMLParser.HTMLParser()
    print(unescape(text))
    return unescape(text)

#fetch html page
url = input("Please enter the url to the site: \n") or "http://stackoverflow.com/questions/138175/dotnetnuke-vulnerabilities"
#parse the domain url of the website
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
k = 0
if(tree.xpath(".//td[@class='post-signature owner']//span[@class='badge1']")!=[]): #if statement to check whether person has these badges.
    num.text = tree.xpath(".//td[@class='post-signature owner']//span[@class='badgecount']/text()")[k]
    k = k+1
else:
    num.text = str(0)
num.tail = "Number of Silver Badges: "
num = etree.SubElement(p,'num')
if(tree.xpath(".//td[@class='post-signature owner']//span[@class='badge2']")!=[]): #if statement to check whether person has these badges.
    num.text = tree.xpath(".//td[@class='post-signature owner']//span[@class='badgecount']/text()")[k]
    k = k+1
else:
    num.text = str(0)
num.tail = "Number of Bronze Badges: "
num = etree.SubElement(p,'num')
if(tree.xpath(".//td[@class='post-signature owner']//span[@class='badge2']")!=[]): #if statement to check whether person has these badges.
    num.text = tree.xpath(".//td[@class='post-signature owner']//span[@class='badgecount']/text()")[k]
    k = k+1
else:
    num.text = str(0)
####
answers_person = tree.xpath(".//div[@id='answers']//div[@class='user-details']")
for i in answers_person:
    if(i.xpath(".//a/text()")!=[]):
        person = etree.SubElement(listPerson,'person')
        person.attrib[etree.QName(g_xml_namespace,"id")] = i.xpath(".//a/text()")[0]
        person.attrib["url"] = i.xpath(".//a/@href")[0]
        #####
        signatureContent = etree.SubElement(person,'signatureContent')
        ######
        p = etree.SubElement(signatureContent,'p')
        p.text = "Reputation: "
        #######
        num = etree.SubElement(p,'num')

        num.text = i.xpath(".//span[@class='reputation-score']/text()")[0]
        num.tail = "Number of Gold Badges: "
        num = etree.SubElement(p,'num')
        k = 0
        if(i.xpath(".//span[@class='badge1']")!=[]):

            num.text = i.xpath(".//span[@class='badgecount']/text()")[k]
            k=k+1
        else:
            num.text = str(0)
        num.tail = "Number of Silver Badges: "
        num = etree.SubElement(p,'num')
        if(i.xpath(".//span[@class='badge2']")!=[]):
            num.text = i.xpath(".//span[@class='badgecount']/text()")[k]
            k=k+1
        else:
            num.text = str(0)
        num.tail = "Number of Bronze Badges: "
        num = etree.SubElement(p,'num')
        if(i.xpath(".//span[@class='badge3']")!=[]):
            num.text = i.xpath(".//span[@class='badgecount']/text()")[k]
            k=k+1
        else:
            num.text = str(0)
##
text = etree.SubElement(TEI,'text')
###
body = etree.SubElement(text,'body')
####
div = etree.SubElement(body,'div')
div.attrib["type"] = "forum"
#####
post = etree.SubElement(div,'post')
post.attrib["when"] = tree.xpath(".//div[@class='question']//td[@class='post-signature owner']//span[@class='relativetime']/@title")[0]
post.attrib["who"] = tree.xpath(".//td[@class='post-signature owner']//div[@class='user-details']/a/text()")[0]
revisedWhen = tree.xpath(".//td[@class='post-signature']//div[@class='user-info ']//span[@class='relativetime']/@title")
if revisedWhen != []:
    post.attrib["revisedWhen"] = revisedWhen[0]
post.attrib["upVote"] = tree.xpath(".//div[@class='question']//td[@class='votecell']//span[@class='vote-count-post ']/text()")[0]
post.attrib["accepted"] = tree.xpath(".//div[@class='question']//td[@class='votecell']//a[@class='star-off']/text()")[0]
#p = etree.SubElement(post,'p')
post.text = ""
for i in tree.xpath(".//div[@class='question']//td[@class='postcell']//div[@class='post-taglist']//a[@rel='tag']"):
    tag = etree.SubElement(p,'tag')
    tag.text = i.xpath("text()")[0]
    post.insert(1,tag)
for i in tree.xpath(".//div[@class='question']//td[@class='postcell']//div[@class='post-text']/*"): #loop to get full post text
    for j in i.xpath("descendant-or-self::text()"): #decendant-or-self gets all text, even with br elements present
        if(i.xpath("name()")=="pre"):   #if tag is 'pre' then get all text from children and put it under code tag. Otherwise just use the tag name of iterator i
            p = etree.SubElement(post,"code")
        else:
            p = etree.SubElement(post,i.xpath("name()"))
        p.text = ""
        p.text += j
        p.tail = ""
        #post.text += i
post.tail = ""


####
moderation = tree.xpath(".//div[@class='question']//td[@class='special-status']")
if moderation != []: #check if there is a special status on post (e.g. post closed)
    ####
    div = etree.SubElement(body,'div')
    div.attrib["type"] = "moderator"
    #####
    head = etree.SubElement(div,'head')
    head.text = " ".join(moderation[0].xpath("div[@class='question-status']//h2/descendant-or-self::*/text()[normalize-space()]"))
    #####
    post = etree.SubElement(div,'post')
    post.attrib["when"] = moderation[0].xpath("div[@class='question-status']//span[@class='relativetime']/@title")[0]
    post.attrib["who"] = moderation[0].xpath("div[@class='question-status']//h2/a/text()")[0]
    post.text = " ".join(moderation[0].xpath("div[@class='question-status']//p/descendant-or-self::*/text()[normalize-space()]"))
    ####
    for i in tree.xpath(".//div[@class='question']//div[@class='comments ']//tr[@class='comment ']"):
        ####
        div = etree.SubElement(body,'div')
        div.attrib["type"] = "response"
        #####
        post = etree.SubElement(div,'post')
        post.attrib["who"] = i.xpath(".//a[@class='comment-user' or @class='comment-user owner']/text()")[0]
        post.attrib["when"] = i.xpath(".//span[@class='relativetime-clean']/@title")[0]
        post.attrib["indentLevel"] = "1"
        ######
        p = etree.SubElement(post,'p')
        p.text =" ".join(i.xpath(".//span[@class='comment-copy']/descendant-or-self::*/text()[normalize-space()]"))
####
for i in tree.xpath(".//div[@id='answers']//div[@class='answer accepted-answer' or @class='answer']"):
    ####
    div = etree.SubElement(body,'div')
    div.attrib["type"] = "answer"
    #####
    post = etree.SubElement(div,'post')
    post.attrib["who"] = i.xpath(".//td[@class='answercell']//div[@class='user-details']/a/text()")[0]
    post.attrib["when"] =i.xpath(".//td[@class='answercell']//div[@class='user-action-time']/span[@class='relativetime']/@title")[0]
    post.attrib["upVote"] = i.xpath(".//td[@class='votecell']//span[@class='vote-count-post ']/text()")[0]
    if(i.xpath("./@class")[0]=="answer accepted-answer"):
        post.attrib["accepted"] = "accepted"
    ######
    post.text = ""
    for j in i.xpath(".//td[@class='answercell']//div[@class='post-text']/*"): #loop to get full post text
        print(etree.tostring(j,encoding='ascii',method="html").decode('utf-8','ignore'))
        post.text += unescape(etree.tostring(j,encoding='ascii',method="html").decode('utf-8','ignore'))
        # print(j.xpath("descendant-or-self::text()"))
        # for k in j.xpath("descendant-or-self::text()"): #decendant-or-self gets all text, even with br elements present #change text to node(), then iterate through it
        #     #for l in k.xpath("text()"):
        #     print(k)
        #     print(j.xpath("text()"))
        #     print(j.xpath("string(descendant-or-self::node())"))
        #     if(j.xpath("name()")=="pre"):   #if tag is 'pre' then get all text from children and put it under code tag. Otherwise just use the tag name of iterator i
        #         p = etree.SubElement(post,"code")
        #     else:
        #         print(j.xpath("name()"))
        #         p = etree.SubElement(post,j.xpath("name()"))
        #     p.text = ""
        #     #print(k.xpath("text()"))
        #     p.text += k
        #     p.tail = ""
        #     #post.text += i
    post.tail = ""

    #p = etree.SubElement(post,'p')
    #p.text =" ".join(i.xpath(".//td[@class='answercell']//div[@class='post-text']/p/descendant-or-self::*/text()[normalize-space()]"))

    ####
    for j in i.xpath(".//div[@class='comments ']//tr[@class='comment ']"):
        ####
        div = etree.SubElement(body,'div')
        div.attrib["type"] = "response"
        #####
        post = etree.SubElement(div,'post')
        post.attrib["who"] = j.xpath(".//a[@class='comment-user' or @class='comment-user owner']/text()")[0]
        post.attrib["when"] = j.xpath(".//span[@class='relativetime-clean']/@title")[0]
        post.attrib["indentLevel"] = "1"
        ######
        p = etree.SubElement(post,'p')
        p.text =" ".join(j.xpath(".//span[@class='comment-copy']/descendant-or-self::*/text()[normalize-space()]"))

# pretty string
s = etree.tostring(TEI,pretty_print=True,encoding='utf-8')
# s_xml = etree.fromstring(s)
# from lxml.html import clean
# s_xml = clean_html(s_xml)
# result = lxml.html.tostring(s_xml, encoding="ascii")
# print(result)
saveToFile(s,"post")
