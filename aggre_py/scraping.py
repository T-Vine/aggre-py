"""
'scraping' creates a Soup of the News Sites, and then scrapes titles, links, and subtitles from the
objects.
Due to the relative time of a request, it should run asynchronously. Promo codes are ignored judging
by the text in a link. 
"""
from os import path
import logging
import logging.config
import asyncio
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from aggre_py import constants as c
from aggre_py.formatting import Formatting

class Scraping:
    """
    Class to Scrape all data from websites. 
    There is no 'init' or constructor method as it is simply for ease of coding, 
    and we don't want instants.
    """
    # Setting up logging.
    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
    # Logging Outfile.
    log_outfile_path = "log.txt"
    file_handler = logging.FileHandler(log_outfile_path, mode="a")
    logging.config.fileConfig(log_file_path)
    # Formatting
    formatted = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)
    file_handler.setFormatter(formatted)
    logger.addHandler(file_handler)
    logger.debug("Online.")

    ind_titles: list[str] = []
    bbc_titles: list[str] = []
    ind_links: list[str] = []
    bbc_links: list[str] = []
    ind_subs: list[str] = []
    bbc_subs: list[str] = []
    
    @staticmethod
    async def to_soup(site: str) -> BeautifulSoup:
        ua = UserAgent
        ua = ua.random
        headers = {"User-Agent": str(ua)}
        """Converts to soup."""
        request = requests.get(site, headers=headers)
        soup = BeautifulSoup(request.content,  "html.parser")
        return soup

    @classmethod
    async def parse_sub_titles(cls, links: list[str], subs_list: list[str], prefix: str,
                             sub_class: str):
        """Scrapes subtitles from individual news links."""
        sub_title: str = ""
        for link in links:
            if link[0:5] != "https":
                ua = UserAgent
                ua = ua.random
                headers = {"User-Agent": str(ua)}
                link = prefix + link
                try:
                    request = requests.get(link, headers=headers)
                    await asyncio.sleep(0.0001)
                    soup = BeautifulSoup(request.content, "html.parser")
                    sub_title = soup.find(attrs={"class": sub_class})
                    subs_list.append(sub_title.get_text())
                except AttributeError:
                    subs_list.append("None") # Adds a spacer so subtitles, titles, etc.
                #can be matched. String type used for ease in later concatenation. This is as
                # NoneType is returned from soup.find.

    @classmethod
    async def parse_main_data(cls, site: str, title: str, titles: list[str], links: list[str]):
        """Scrapes headers and links from the soup."""
        text: str = ""
        soup = await cls.to_soup(site)

        for i in soup.find_all(attrs={"class": title}):
            text = i.get_text()
            if i.get("href") is None:
                pass
            else:
                # Ignoring unwanted extras.
                if text in ('Scotland', 'ALBA', 'Wales', 'Cymru', 'NI'):
                    pass
                elif "voucher" not in i.get("href"): # Ignoring if it is a promo link.
                    if ("Audio" or "Video") in text and "minutes" in text \
                    and site != c.INDEPENDENT: # Ignoring audio/video.
                        index = text.find("minutes") + 7
                        text = text[index: ]

                    titles.append(text)
                    links.append(i.get("href"))

    @classmethod
    async def main(cls):
        """Main function that calls the others."""
        await asyncio.gather(cls.parse_main_data(c.INDEPENDENT, c.IND_TITLE, cls.ind_titles,
                                                 cls.ind_links), cls.parse_main_data(c.BBC, 
                                                c.BBC_TITLE, cls.bbc_titles, cls.bbc_links))
                                                 
        await asyncio.gather(cls.parse_sub_titles(cls.ind_links, cls.ind_subs, c.INDEPENDENT,
                                                  c.IND_SUBS), cls.parse_sub_titles(cls.bbc_links,
                                                cls.bbc_subs, c.BBC, c.BBC_SUBS))
                                                  
        await asyncio.gather(Formatting.write("independent.txt", cls.ind_titles, cls.ind_subs,
                                                cls.ind_links, c.INDEPENDENT), Formatting.write("bbc.txt",
                                                cls.bbc_titles, cls.bbc_subs, cls.bbc_links, c.BBC))

if __name__ == "__main__":
    asyncio.run(Scraping.main())
    print(Scraping.indTitles)
    