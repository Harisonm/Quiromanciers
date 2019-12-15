from lesQuiromanciers.api.wikipedia.WikiFactory import WikiFactory
from lesQuiromanciers.model.CharLSTMModel import CharLSTMModel
import pandas as pd
import csv
import os

filename = "data/biographie_df.csv"

if __name__ == "__main__":

    # One shot -> create csv
    # test = WikiFactory().build_biographie()

    clstm = CharLSTMModel()

    df_biographie = pd.read_csv(filename, encoding="utf-8", sep=";")
    print(df_biographie.head())

    clstm.fit(df_biographie, epochs=10)
    clstm.generate("indubitably ")

    # text = "\n".join([" ".join(sentence) for sentence in chunk["biographie"]])

