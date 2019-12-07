from lesQuiromanciers.api.wikipedia.WikiFactory import WikiFactory
from lesQuiromanciers.model.charLSTMmodel import charLSTMmodel
import pandas as pd
import csv

if __name__ == "__main__":

    # One shot -> create csv
    # test = WikiFactory().build_biographie()

    # df = pd.read_csv("data/ biographie_df.csv", encoding="utf-8", sep=";")
    # print(df["biographie"])
    with open("data/biographie_df.csv", "r") as f:
        reader = csv.reader(f)
        your_list = list(reader)
    # print(your_list)

    # text = "\n".join([" ".join(sentence) for sentence in your_list])
    # print(text)
    # clstm = charLSTMmodel()
    # clstm.fit(text, epochs=1)

