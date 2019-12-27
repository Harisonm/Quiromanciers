from lesQuiromanciers.model.GenerationBioModel import GenerationBioModel
import pandas as pd
import csv
import os

filename = "data/biographie_df.csv"

if __name__ == "__main__":

    # One shot -> create csv
    # test = WikiFactory().build_biographie()
    biographie_df = pd.read_csv(filename, encoding="utf-8", sep=";", usecols = ['name', 'biographie'])
    clstm = GenerationBioModel()
    clstm.fit(biographie_df, epochs=1)


    # clstm.generate("indubitably ")

