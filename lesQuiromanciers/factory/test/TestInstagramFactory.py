from lesQuiromanciers.factory.InstagramFactory import InstagramFactory
from lesQuiromanciers.model.instagram.InstagramClassification import (
    InstagramClassification,
)
import pandas as pd
import csv
import os
import datetime as dt

if __name__ == "__main__":

    # Récupérer les données d'instagram sous forme de DataFrame
    instaData = InstagramFactory(
        [
            "marty_the_cockerdale",
            "lecoindespatissiers",
            "cataniafoodprn",
            "guatemala_magica",
            "justinmin",
        ],
        dt.datetime(2019, 1, 1),
        dt.datetime(2019, 12, 31),
    )
    instaData.download_data()
    instaData.dataframe_creation()

    # Classer les utilisateurs selon Traveler et/ou Foody
    instaClassifier = InstagramClassification(instaData.dataframe_creation())
    classification = instaClassifier.result()
    classification.to_csv(r"data/classification.csv")
