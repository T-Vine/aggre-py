"""
'scraping' creates a Soup of the News Sites, and then scrapes titles, links, and subtitles from the objects.
Due to the relative time of a request, it should run asynchronously. Promo codes are ignored judging by the text in a link. 
"""
from bs4 import BeautifulSoup
import requests
import time
import constants as c

# Globals.
indTitles: list[str] = []
bbcTitles: list[str] = []

indLinks: list[str] = []
bbcLinks: list[str] = []

start_time = time.time()

def toSoup(site: str) -> BeautifulSoup:
    request = requests.get(site)
    soup = BeautifulSoup(request.content,  "html.parser")
    return soup 

def parseMainData(soup: BeautifulSoup, title: str, titles: list[str], links: list[str]): 
    for i in soup.find_all(attrs={"class": title}):
        if (i.get("href") == None):
            pass    
        else:
            if "voucher" not in i.get("href"): # Ignoring if it is a promo link.
                titles.append(i.get_text())
                links.append(i.get("href"))
            
def main():
    soup = toSoup(c.INDEPENDENT)
    parseMainData(soup, c.IND_TITLE, indTitles, indLinks)
    print(indTitles)


if (__name__ == "__main__"):
    main()

end_time = time.time() - start_time


print(end_time)