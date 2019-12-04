#!/usr/bin/python3
from SPARQLWrapper import SPARQLWrapper, JSON
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


def get_person_name():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(
        """
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
    PREFIX p: <http://www.wikidata.org/prop/> 
    PREFIX psv: <http://www.wikidata.org/prop/statement/value/> 
    PREFIX bd: <http://www.bigdata.com/rdf#> 
    PREFIX wikibase: <http://wikiba.se/ontology#> 
    PREFIX wd: <http://www.wikidata.org/entity/> 
    PREFIX wdt: <http://www.wikidata.org/prop/direct/> 

    select 
    ?personLabel
    where {
        ?person wdt:P31 wd:Q5 . 
        ?person wdt:P106 wd:Q33999
    
    # Doc : https://www.mediawiki.org/wiki/Wikidata_query_service/User_Manual#Label_service
    # SELECT ?variableLabel ?variableAltLabel  ?variableDescription
    SERVICE wikibase:label {
        bd:serviceParam wikibase:language "fr,en" .
    }
    } LIMIT 3"""
    )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

    # print(result["label"]["value"])


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
    names = []
    name_people = get_person_name()

    for result in name_people["results"]["bindings"]:
        names.append(result["personLabel"]["value"])

    print(names)
    search = "Nelson Mandela"

    df = pd.DataFrame(columns=["name", "biographie"])
    for name in names:
        if searchPages(name):
            df = df.append(
                {"name": name, "biographie": wikipedia.page(name).content},
                ignore_index=True,
            )
    print(df)
