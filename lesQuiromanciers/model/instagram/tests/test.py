from lesQuiromanciers.api.instagram.InstagramFactory import InstaFactory
from lesQuiromanciers.model.insta_model.InstagramClassification import InstagramClassification
import pandas as pd
import csv
import os
import datetime as dt


if __name__ == "__main__":

    # Récupérer les données d'instagram sous forme de DataFrame
    instaData = InstaFactory(["marty_the_cockerdale", "lecoindespatissiers", "cataniafoodprn", "guatemala_magica", "justinmin"],
                     dt.datetime(2019, 1, 1),
                     dt.datetime(2019, 12, 31))
    instaData.download_data()
    instaData.dataframe_creation()

    #Classer les utilisateurs selon Traveler et/ou Foody
    instaClassifier = ClassificationInstagram(instaData.dataframe_creation())
    classification = instaClassifier.result()
    classification.to_csv(r'data/classification.csv')
