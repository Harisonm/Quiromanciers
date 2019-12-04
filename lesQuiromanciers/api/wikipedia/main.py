#!/usr/bin/python3


import requests
from bs4 import BeautifulSoup


session = requests.Session()
url = "https://en.wikipedia.org/w/api.php"


def searchPages(search):
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": search
    }

    response = session.get(url=url, params=params)
    data = response.json()

    if data['query']['search'][0]['title'] == search:
        print("Your search page '" + search + "' exists on English Wikipedia")


def getPage(pageId):
    params = {
        "action": "parse",
        "pageid": pageId,
        "format": "json",
    }

    response = session.get(url=url, params=params)
    data = response.json()
    cleaned_data = cleanData(data["parse"]["text"]["*"])
    print(cleaned_data)


def cleanData(text):
    soup = BeautifulSoup(text)

    for item in soup.find_all("h2", id="See_also").find_all_next(string=True):
        item.decompose()

    text = soup.get_text()
    return text


if __name__ == "__main__":
    search = "Nelson Mandela"
    pageId = 21492751

    #searchPages(search)
    getPage(pageId)

