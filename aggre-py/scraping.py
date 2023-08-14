from bs4 import BeautifulSoup
import requests
import constants as c

# Globals.
titles = []
links = []

request = requests.get(c.INDEPENDENT)
soup = BeautifulSoup(request.content,  "html.parser")

for i in soup.find_all(attrs={"class": c.IND_TITLE}):
    if i.get("href") == None:
        pass
    else:
        if "voucher" not in i.get("href"): # Ignoring if it is a promo link.
            titles.append(i.get_text())
            links.append(i.get("href"))

print(titles)
print(links)