"""
'scraping' creates a Soup of the News Sites, and then scrapes titles, links, and subtitles from the objects.
Due to the relative time of a request, it should run asynchronously. Promo codes are ignored judging by the text in a link. 
"""
from bs4 import BeautifulSoup
import requests
import time
import asyncio
import constants as c

# Globals.
indTitles: list[str] = []
bbcTitles: list[str] = []

indLinks: list[str] = []
bbcLinks: list[str] = []

start_time = time.time()

async def toSoup(site: str) -> BeautifulSoup:
    request = requests.get(site)
    soup = BeautifulSoup(request.content,  "html.parser")
    return soup 

async def parseMainData(site: str, title: str, titles: list[str], links: list[str]): 
    text: str = ""
    soup = await toSoup(site)
    
    for i in soup.find_all(attrs={"class": title}):
        text = i.get_text()
        if (i.get("href") == None):
            pass    
        else:
            # Ignoring unwanted extras.
            if (text == "Scotland") or (text == "ALBA") or (text == "Wales") or (text == "Cymru") or (text == "NI"):
                    pass
            elif ("voucher" not in i.get("href")): # Ignoring if it is a promo link.
                if 'Audio' or 'Video' in text: # Ignoring audio/video.
                        index = text.find("minutes") + 7
                        text = text[index: ]
                
                titles.append(text)
                links.append(i.get("href"))
            
async def main():
    await asyncio.gather(parseMainData(c.INDEPENDENT, c.IND_TITLE, indTitles, indLinks), 
                        parseMainData(c.BBC, c.BBC_TITLE, bbcTitles, bbcLinks))
    print(indTitles)
    print(bbcTitles)


if (__name__ == "__main__"):
    asyncio.run(main())
    end_time = time.time() - start_time
    print(end_time)

