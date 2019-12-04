#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import wikipedia
import pandas as pd
import black

session = requests.Session()
url = "https://en.wikipedia.org/w/api.php"


def searchPages(search: str) -> bool:
    params = {"action": "query", "format": "json", "list": "search", "srsearch": search}
    response = session.get(url=url, params=params)
    data = response.json()

    if data["query"]["search"][0]["title"] == search:
        print("Your search page '" + search + "' exists on English Wikipedia")
        return True
    else:
        return False


# def getPage(pageId):
#     params = {
#         "action": "parse",
#         "pageid": pageId,
#         "format": "json",
#     }

#     response = session.get(url=url, params=params)
#     data = response.json()
#     cleaned_data = cleanData(data["parse"]["text"]["*"])
#     print(cleaned_data)


# def cleanData(text):
#     soup = BeautifulSoup(text)

#     for item in soup.find_all_next(string=True,name="h2", id="See_also"):
#         item.decompose()

#     text = soup.get_text()
#     return text

# def get_page_id(self):
#     pass


if __name__ == "__main__":

    # #pageId = 21492751
    # searchPages(search)
    # #getPage(pageId)

    search = "Nelson Mandela"
    df = pd.DataFrame(columns=["name", "biographie"])
    if searchPages(search):
        df = df.append(
            {"name": search, "biographie": wikipedia.page(search).content},
            ignore_index=True,
        )

    print(df)
