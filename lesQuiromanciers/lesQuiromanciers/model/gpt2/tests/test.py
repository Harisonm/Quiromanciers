from lesQuiromanciers.api.wikipedia.WikiFactory import WikiFactory
from lesQuiromanciers.model.gpt2_model.BiographieGenerator import BiographieGenerator
import pandas as pd
import csv
import os
import datetime as dt

filename = "data/biographie_df.csv"

if __name__ == "__main__":

    # One shot -> create csv
    # test = WikiFactory().build_biographie()
    biographie_df = pd.read_csv(
        filename, encoding="utf-8", sep=";", usecols=["name", "biographie"]
    )

    test = BiographieGenerator(model_name="124M", file_name="biographie.txt")
