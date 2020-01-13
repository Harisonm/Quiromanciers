from lesQuiromanciers.model.model_tf.GenerationBioModel import GenerationBioModel
from lesQuiromanciers.api.instagram.InstagramFactory import InstaFactory
from lesQuiromanciers.model.insta_model.InstagramClassification import InstagramClassification
import pandas as pd
import csv
import os
import datetime as dt

filename = "data/biographie_df.csv"

if __name__ == "__main__":

    # One shot -> create csv
    # test = WikiFactory().build_biographie()
    
    
    # biographie_df = pd.read_csv(
    #     filename, encoding="utf-8", sep=";", usecols=["name", "biographie"]
    # )
    # clstm = GenerationBioModel()
    # clstm.fit(biographie_df, epochs=50)

    # # clstm.generate("indubitably ")

    # # Récupérer les données d'instagram sous forme de DataFrame
    # instaData = InstaFactory(["marty_the_cockerdale", "lecoindespatissiers", "cataniafoodprn", "guatemala_magica", "justinmin"],
    #                  dt.datetime(2019, 1, 1),
    #                  dt.datetime(2019, 12, 31))
    # instaData.download_data()
    # instaData.dataframe_creation()

    # #Classer les utilisateurs selon Traveler et/ou Foody
    # instaClassifier = ClassificationInstagram(instaData.dataframe_creation())
    # classification = instaClassifier.result()
    # classification.to_csv(r'data/classification.csv')
