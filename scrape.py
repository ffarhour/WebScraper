from lxml import html
import requests

page = requests.get('http://stackoverflow.com/questions/8692/how-to-use-xpath-in-python')
tree = html.fromstring(page.content)
content=tree.xpath('//title/text()')
print(content)