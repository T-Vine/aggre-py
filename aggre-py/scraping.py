from bs4 import BeautifulSoup
import requests
import constants as c


request = requests.get(c.INDEPENDENT)
soup = BeautifulSoup(request.content,  "lxml-xml")
titles = []
for i in soup.find_all(attrs={"class": c.IND_TITLE}):
    titles.append(i)
