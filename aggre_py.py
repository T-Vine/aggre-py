"""
The main file for aggre-py.
"""
import asyncio
import logging
import logging.config
from os import path
from aggre_py.scraping import Scraping

# Setting up logging.
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'aggre_py\logging.conf')
# Logging Outfile.
log_outfile_path = path.join(path.dirname(path.abspath(__file__)), "log.txt")
file_handler = logging.FileHandler(log_outfile_path, mode="a")
logging.config.fileConfig(log_file_path)

# Formatting
formatted = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
mainLogger = logging.getLogger(__name__)
file_handler.setFormatter(formatted)
mainLogger.addHandler(file_handler)

if __name__ == "__main__":
    mainLogger.debug("Online")
    asyncio.run(Scraping.main())
    