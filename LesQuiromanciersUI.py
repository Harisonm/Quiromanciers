import streamlit as st
import pandas as pd
import numpy as np
import requests
from lesQuiromanciers.model.gpt2_model.BiographieGenerator import BiographieGenerator

file_name = st.text_input('give file name')
st.write('csv file name', file_name)

submit = st.button('submit new letters')
if submit:
    biographie_df = pd.read_csv(
        filename, encoding="utf-8", sep=";", usecols=["name", "biographie"]
    )
    
    test = BiographieGenerator(model_name="124M",file_name="biographie.txt")
    
def load_data(file_name):
    WikiFactory().build_biographie(file_name)
    print("ok")
    return "Done"

def generate_biographie(seed):
    pass
# requests.get('http://0.0.0.0:5000/wiki/<file_name>', json=new_candidates)