from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re


# url = "https://edition.cnn.com/"
#
# page = urlopen(url)
#
# html_bytes = page.read()
# html = html_bytes.decode('utf-8')
#
# soup = BeautifulSoup(html, 'html.parser')
# for link in soup.find_all('a'):
#     print(link.get("href"))

url = Request("https://edition.cnn.com/")

page = urlopen(url)

url_html_bytes = page.read()
url_html = url_html_bytes.decode('utf-8')

soup = BeautifulSoup(url_html, 'html.parser')
for article in soup.findAll('li'):
    pass