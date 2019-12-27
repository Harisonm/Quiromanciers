from lesQuiromanciers.model.GenerationBioModel import GenerationBioModel
import pandas as pd
import csv
import os

filename = "data/biographie_df.csv"

if __name__ == "__main__":

    # One shot -> create csv
    # test = WikiFactory().build_biographie()
    df_biographie = pd.read_csv(filename, encoding="utf-8", sep=";")
    print(df_biographie[df_biographie['name'] == "Justin Bieber"].biographie)

    # clstm = GenerationBioModel()
    # clstm.fit(filename, epochs=25)


    # clstm.generate("indubitably ")

