"""
'scraping' creates a Soup of the News Sites, and then scrapes titles, links, and subtitles from the objects.
Due to the relative time of a request, it should run asynchronously. Promo codes are ignored judging by the text in a link. 
"""



from bs4 import BeautifulSoup
import requests
import time
import constants as c

# Globals.
titles = []
links = []

start_time = time.time()

request = requests.get(c.INDEPENDENT)
soup = BeautifulSoup(request.content,  "html.parser")

for i in soup.find_all(attrs={"class": c.IND_TITLE}):
    if i.get("href") == None:
        pass    
    else:
        if "voucher" not in i.get("href"): # Ignoring if it is a promo link.
            titles.append(i.get_text())
            links.append(i.get("href"))

end_time = time.time() - start_time

print(titles)
print(links)
print(end_time)