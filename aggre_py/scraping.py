"""
'scraping' creates a Soup of the News Sites, and then scrapes titles, links, and subtitles from the objects.
Due to the relative time of a request, it should run asynchronously. Promo codes are ignored judging by the text in a link. 
"""
from bs4 import BeautifulSoup
import requests
import time
import asyncio
from os import path
import logging
import logging.config
from . import constants as c

class Scraping:
     # Setting up logging.
    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
    # Logging Outfile.
    log_outfile_path = path.join(path.dirname(path.abspath(__file__)), "log.txt")   
    file_handler = logging.FileHandler(log_outfile_path, mode="a")
    logging.config.fileConfig(log_file_path)    
    # Formatting
    format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)
    file_handler.setFormatter(format)
    logger.addHandler(file_handler)
    logger.debug("Online.")
    
    indTitles: list[str] = []
    bbcTitles: list[str] = []

    indLinks: list[str] = []
    bbcLinks: list[str] = []
    
    indSubs: list[str] = []

    @staticmethod
    async def toSoup(site: str) -> BeautifulSoup:
        request = requests.get(site)
        soup = BeautifulSoup(request.content,  "html.parser")
        return soup 

    @classmethod
    async def parseSubTitles(cls, site: str):
        subTitle: str = ""
        if (site == c.INDEPENDENT):
            for link in cls.indLinks:
                if (link[0:5] != "https"):
                    link = "https://www.independent.co.uk" + link
                try:
                    r = requests.get(link)
                    soup = BeautifulSoup(r.content, "html.parser")
                    subTitle = soup.find(attrs={"class": c.IND_SUBS})
                    cls.indSubs.append(subTitle.get_text())
                except:
                    pass # Subtitle not found.
        else:
            pass # BBC functionality not yet added.
                
    @classmethod
    async def parseMainData(cls, site: str, title: str, titles: list[str], links: list[str]): 
        text: str = ""
        soup = await cls.toSoup(site)
    
        for i in soup.find_all(attrs={"class": title}):
            text = i.get_text()
            if (i.get("href") == None):
                pass    
            else:
                # Ignoring unwanted extras.
                if (text == "Scotland") or (text == "ALBA") or (text == "Wales") or (text == "Cymru") or (text == "NI"):
                        pass
                elif ("voucher" not in i.get("href")): # Ignoring if it is a promo link.
                    if ("Audio" or "Video" in text) and ("minutes" in text) and (site != c.INDEPENDENT): # Ignoring audio/video.
                            index = text.find("minutes") + 7
                            text = text[index: ]
                
                    titles.append(text)
                    links.append(i.get("href"))
        
        await cls.parseSubTitles(site)
                    
    @classmethod        
    async def main(cls):
        await asyncio.gather(cls.parseMainData(c.INDEPENDENT, c.IND_TITLE, cls.indTitles, cls.indLinks), 
                            cls.parseMainData(c.BBC, c.BBC_TITLE, cls.bbcTitles, cls.bbcLinks))


if (__name__ == "__main__"):
    start_time = time.time()
    asyncio.run(Scraping.main())
    end_time = time.time() - start_time
    print(Scraping.indTitles)
    print(end_time)
    

