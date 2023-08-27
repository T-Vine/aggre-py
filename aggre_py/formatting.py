"""
Controls formatting: currently writing to files only.
"""
from os import path
import logging
import logging.config

class Formatting:
    """Formats Data"""
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

    @staticmethod
    async def write(file: str, titles: list[str], subs: list[str], links: list[str]):
        """Writes to files."""
        new_line = "\n"
        with open(file, "w", encoding="utf8") as my_file:
            for k, j, i in zip(titles, subs, links):
                my_file.write(k + new_line)
                my_file.write(j + new_line)
                my_file.write(i + new_line)
