#!/usr/bin/python3
from bs4 import BeautifulSoup
from traceback import print_exc
import requests
import wikipedia
import pandas as pd
import re

session = requests.Session()
url = "https://en.wikipedia.org/w/api.php"


class WikiFactory(object):
    def __init__(self):
        pass

    def __searchPages(self, search: str):
        """
        __searchPages : Function qui vas chercher les pages des entités que l'on passe dans l'argument search
        
        Args:
            search (str): nom d'un entités (auteur, commedien, acteur..).
        
        Returns:
            bool: True pour page trouvé, sinon False pour non trouvé.
        """
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

    def __get_person_name(self,name_file_source):
        """
        __get_person_name : Fonction qui vas lire un fichier pour le stocker dans un dataframe
        
        Returns:
            pd.DataFrame: Dataframe de type Pandas
        """
        try:
            df = pd.read_csv(name_file_source, header=None, encoding="utf-8", sep=";")
            return df
        except:
            print_exc()

    @staticmethod
    # TO DO : write this with multithreading using concurrent.futures.ProcessPoolExecutor with executor.submit
    def __get_biographie(name):
        """
        __get_biographie : Fonction qui permet d'obtenir la page biographie d'eune personne.
        
        Args:
            name (str): Nom de la personne a chercher 
        
        Returns:
            str : La page biographie wikipedia de la personne passé en argument.
        """
        try:
            return wikipedia.page(name).content
        except:
            print_exc()
    
    @staticmethod        
    def clean_data(words):
        """
        clean_data : Mise au propre des données du dataframe
        
        Args:
            words (str): Les mots de la biographie
        
        Returns:
            str: Les mots mise au propre
        """
        words = str(words)
        words = re.sub(r'\(.*?\)', '', words)
        words = re.sub(r'\[.*?\]', '', words)
        return words
    
    @staticmethod
    def tag_name(words):
        """
        tag_name : fonction qui permet de tagger les noms dans les biographies afin de les tranformer par #nature
        
        Args:
            words (list): biographie stocké dans une liste.
        
        Returns:
            list: Biographie taggé stocker dans une liste 
        """
        name = str(words[0])
        names = name.split(' ')
        bio = words[1]
        if ' , known ' in bio[0:50]:
            bio = re.sub('^.* , known ' , '#name , known ', bio)
        if ' is ' in bio[0:50]:
            bio = re.sub('^.* is ' , '#name is ', bio)
        if ' was ' in bio[0:50]:
            bio = re.sub('^.* was ' , '#name was ', bio)
        bio = bio.replace(name, '#name')
        for n in names:
            bio = bio.replace(n, '#name')
        return bio

    def build_biographie(self,file_name_source, file_name_destination):
        """
        build_biographie : Construit la biographie a partir des noms des entités (personne)
        
        Args:
            file_name_source (str): Nom du fichier d'entée.
            file_name_destination(str): Nom du fichier de sortie.
        """
        df_biographie = pd.DataFrame(columns=["name", "biographie"])
        
        name_people = self.__get_person_name(file_name_source)

        for index, row in name_people.iterrows():
            try:
                if self.__searchPages(row.values):
                    df_biographie = df_biographie.append(
                        {
                            "name": row.values,
                            "biographie": self.__get_biographie(row.values),
                        },
                        ignore_index=True,
                    )
                    print(df_biographie)
            except:
                print_exc()
                
        try:
            
            df_biographie["biographie"] = df_biographie["biographie"].apply(lambda words: self.clean_data(words))
            df_biographie["biographie_taged"] = df_biographie.apply(lambda x: self.tag_name(x), axis=1)
            df_biographie = df_biographie.drop(columns="biographie")
            df_biographie = df_biographie.drop(columns="name")
            
            df_biographie.to_csv(
                path_or_buf=file_name_destination,
                encoding="utf-8",
                sep=";",
                index=False,
                )
            
        except:
            print_exc()
            
        return True
        

