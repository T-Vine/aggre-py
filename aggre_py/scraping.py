"""
'scraping' creates a Soup of the News Sites, and then scrapes titles, links, and subtitles from the objects.
Due to the relative time of a request, it should run asynchronously. Promo codes are ignored judging by the text in a link. 
"""
from bs4 import BeautifulSoup
import requests
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
    bbcSubs: list[str] = []

    @staticmethod
    async def toSoup(site: str) -> BeautifulSoup:
        request = requests.get(site)
        soup = BeautifulSoup(request.content,  "html.parser")
        return soup 

    @classmethod
    async def parseSubTitles(cls, links: list[str], subsList: list[str], prefix: str, subClass: str):
        subTitle: str = ""
        for link in links:
            if (link[0:5] != "https"):
                link = prefix + link
            try:
                r = requests.get(link)
                await asyncio.sleep(0.0001)
                soup = BeautifulSoup(r.content, "html.parser")
                subTitle = soup.find(attrs={"class": subClass})
                subsList.append(subTitle.get_text())
            except:
                subsList.append("None") # Adds a spacer so subtitles, titles, etc. can be matched. String type used for ease in later concatenation.
                
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
    
    @staticmethod
    async def write(file: str, titles: list[str], subs: list[str], links: list[str]):
        newLine = "\n"
        with open(file, "w") as myFile:
            for a, b, c in zip(titles, subs, links):
                myFile.write(a + newLine)
                myFile.write(b + newLine)
                myFile.write(c + newLine)
    
    @classmethod        
    async def main(cls):
        await asyncio.gather(cls.parseMainData(c.INDEPENDENT, c.IND_TITLE, cls.indTitles, cls.indLinks), 
                            cls.parseMainData(c.BBC, c.BBC_TITLE, cls.bbcTitles, cls.bbcLinks))
        await asyncio.gather(cls.parseSubTitles(cls.indLinks, cls.indSubs, c.INDEPENDENT, c.IND_SUBS), 
                             cls.parseSubTitles(cls.bbcLinks, cls.bbcSubs, c.BBC, c.BBC_SUBS))
        await asyncio.gather(cls.write("independent.txt", cls.indTitles, cls.indSubs, cls.indLinks),
                             cls.write("bbc.txt", cls.bbcTitles, cls.bbcSubs, cls.bbcLinks))


if (__name__ == "__main__"):
    asyncio.run(Scraping.main())
    print(Scraping.indTitles)
    

