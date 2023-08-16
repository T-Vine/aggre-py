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
import constants as c

# Setting up logging.
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
# Logging Outfile.
log_outfile_path = path.join(path.dirname(path.abspath(__file__)), "log.txt")
fh = logging.FileHandler(log_outfile_path)
logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)
logger.addHandler(fh)


class Scraping:
    indTitles: list[str] = []
    bbcTitles: list[str] = []

    indLinks: list[str] = []
    bbcLinks: list[str] = []

    @staticmethod
    async def toSoup(site: str) -> BeautifulSoup:
        request = requests.get(site)
        soup = BeautifulSoup(request.content,  "html.parser")
        return soup 

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
                    
    @classmethod        
    async def main(cls):
        await asyncio.gather(cls.parseMainData(c.INDEPENDENT, c.IND_TITLE, cls.indTitles, cls.indLinks), 
                            cls.parseMainData(c.BBC, c.BBC_TITLE, cls.bbcTitles, cls.bbcLinks))


if (__name__ == "__main__"):
    logger.debug('Online.')
    start_time = time.time()
    asyncio.run(Scraping.main())
    end_time = time.time() - start_time
    print(Scraping.indTitles)
    print(end_time)
    

