# aggre-py
 
## About
_aggre-py_ is a python program designed to scrape news articles from popular sites. At the moment it is capable of scraping headlines, subtitles and links to allow users to consider articles thoroughly before opening.
I have perused the ToS of the news sites scraped, however if any changes are made I will of course deprecate them. 
Note how news articles may be a few hours old due to problems with requests. I would have used Selenium, but preferred a more lightweight option.
Note that requests to the BBC may need some timeouts, and sometimes it is better to just run via the independent. Access to this via the command line will be added in the future.

## Contributions
Contributions are welcome via forking and creating a new branch, then submitting a pull request. I will remove them myself, if any are received.

## Developer Usage
I will create a docs file for this in the future: if it has been made, feel free to check it out.
Submit issues via the github issue tracker.

## Background
For me, this project was the culmination of my pure Python journey. Similarly to my Javascript clocks library, I wanted something that could stretch me, and teach me new things. Despite not being that large a project, I have planned it carefully, and made sure to keep it ready for expansions, which was the major idea. There were many things which I wanted to include in this, and have succeeded in doing so:
- Type Hints
- Docstrings
- Asynchronous Programming
- OOP
- Linting
- Different types of methods, though I strayed away from 'getters' and 'setters' due to not needing them.
- Modules
- Do Not Repeat Yourself approach (DNR), a popular coding paradigm one might call it.
- Executable Files
- And general Python etiquette.
Being an amateur developer, I really wanted to increase my own skills in developing. I believe I have, and hopefully I will be able to continue with this project to increase my skills further. While the overall goal seemed simple, it took a lot of effort to get to this point - and many cups of tea! Asyncio was something I thought I would never understand, but I think I finally do. In doing it this way, I both taught myself something new and sped up the program (especially for future functionality). I did however stay away from 'async for', though I experimented with it, as it would not have been overly useful for the context.

## General usage
To use, download the executable and run it. Enter the directory you wanted, with a folder called 'aggre-py' appended to it. Then double click 'aggre-py.py' whenever you want to run, and peruse the conglomerated text files.

## Future Plans
As mentioned, I plan to create an executable (done). I am also interested in creating a GUI for it, or at least something searchable. Given time, and as a break from my other projects, I may create an additional AI to analyse the actual articles, in order to explore that side of python.