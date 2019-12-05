#!/usr/bin/python3
from SPARQLWrapper import SPARQLWrapper, JSON
import requests
from bs4 import BeautifulSoup
import wikipedia
import pandas as pd

session = requests.Session()
url = "https://en.wikipedia.org/w/api.php"


class WikiFactory(object):
    def __init__(self):
        pass

    def __searchPages(self, search: str) -> bool:
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": search,
        }
        response = session.get(url=url, params=params)
        data = response.json()

        if data["query"]["search"][0]["title"] == search:
            print("Your search page '" + search + "' exists on English Wikipedia")
            return True
        else:
            return False

    def __get_person_name(self):
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
            # ?person wdt:P106 wd:Q33999
        
        # Doc : https://www.mediawiki.org/wiki/Wikidata_query_service/User_Manual#Label_service
        # SELECT ?variableLabel ?variableAltLabel  ?variableDescription
        SERVICE wikibase:label {
            bd:serviceParam wikibase:language "fr,en" .
        }
        } LIMIT 10"""
        )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results

    def get_biographie(self):
        names = []
        name_people = self.__get_person_name()

        for result in name_people["results"]["bindings"]:
            names.append(result["personLabel"]["value"])
        print(names)

        df = pd.DataFrame(columns=["name", "biographie"])
        for name in names:
            if self.__searchPages(name):
                df = df.append(
                    {"name": name, "biographie": wikipedia.page(name).content},
                    ignore_index=True,
                )
        print(df)
