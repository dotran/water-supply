#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import platform
from selenium import webdriver
from bs4 import BeautifulSoup


# Check Python version
# print(platform.python_version())

# Using the right PhantomJS for the corresponding OS
if platform.system() == "Windows":
    PHANTOMJS_EXE = "./PhantomJS/phantomjs.exe"
else:
    PHANTOMJS_EXE = "./PhantomJS/phantomjs"


def main():
    # Use PhantomJS to browse the page, alternatively we can use
    # browser = webdriver.Firefox()
    browser = webdriver.PhantomJS(PHANTOMJS_EXE)
    browser.get('http://www.scoreboard.com/en/tennis/atp-singles/us-open-2015/results/')
    
    # Parse the html source
    soup = BeautifulSoup(browser.page_source, "html.parser")
    
    # Get all the games
    games = soup.find_all('tr', {'class': 'stage-finished'})
    
    # Print out the html for the first game
    print(games[0].prettify())


if __name__ == "__main__":
    main()
    # print("This Python script was started as the main program.")
else:
    print("This Python script is to be called as main(), not as the module ", __name__ + ".")
