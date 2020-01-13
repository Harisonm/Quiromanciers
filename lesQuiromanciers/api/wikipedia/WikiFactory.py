#!/usr/bin/python3
from bs4 import BeautifulSoup
from traceback import print_exc
import requests
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
        try:
            df = pd.read_csv("data/people.csv", header=None, encoding="utf-8", sep=";")
            return df
        except:
            print_exc()

    @staticmethod
    # TO DO : write this with multithreading using concurrent.futures.ProcessPoolExecutor with executor.submit
    def __get_biographie(name):
        try:
            return wikipedia.page(name).content
        except:
            print_exc()

    def build_biographie(self,file_name):
        biographie_df = pd.DataFrame(columns=["name", "biographie"])
        name_people = self.__get_person_name()

        for index, row in name_people.iterrows():
            try:
                if self.__searchPages(row.values):
                    biographie_df = biographie_df.append(
                        {
                            "name": row.values,
                            "biographie": self.__get_biographie(row.values),
                        },
                        ignore_index=True,
                    )
                    print(biographie_df)
            except:
                print_exc()

        biographie_df.to_csv(
            path_or_buf=file_name,
            encoding="utf-8",
            sep=";",
            index=False,
        )
