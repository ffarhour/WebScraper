import re
url = "http://stackoverflow.com/questions/36917042/pairwise-circular-python-for-loop"

# import mechanize
#
# # http://stackoverflow.com/questions/14857342/http-403-error-retrieving-robots-txt-with-mechanize
#
# ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0 (compatible;)'
# br = mechanize.Browser()
# br.addheaders = [('User-Agent', ua), ('Accept', '*/*')]
# br.open("http://stackoverflow.com/questions/36917042/pairwise-circular-python-for-loop")
# # follow second link with element text matching regular expression
# response1 = br.follow_link(text_regex=r"show 4 more comments", nr=0)
# assert br.viewing_html()
# print (br.title())
# print (response1.geturl())
# print (response1.info())  # headers
# #print (response1.read())  # body
# text = response1.read()


from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get(url)
#http://selenium-python.readthedocs.io/locating-elements.html?highlight=find_element
#http://stackoverflow.com/questions/27966080/how-to-simulate-mouse-click-on-blank-area-in-website-by-selenium-ide
for element in driver.find_elements_by_xpath(".//a[@title='expand to show all comments on this post' and string-length(text()) > 0]"):
    print(element)
    element.click()
#http://stackoverflow.com/questions/22739514/how-to-get-html-with-javascript-rendered-sourcecode-by-using-selenium
from time import sleep # this should go at the top of the file
sleep(5)
html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
text = html.encode("utf-8")
print(text)
f = open("test.html", 'wb')
f.write(text)
f.close()
#driver.close()
