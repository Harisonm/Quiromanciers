import streamlit as st
import pandas as pd
import numpy as np
import requests
from lesQuiromanciers.model.gpt2.BiographieGenerator import BiographieGenerator
from lesQuiromanciers.factory.InstagramFactory import InstagramFactory
from lesQuiromanciers.factory.WikiFactory import WikiFactory


prefix = st.text_input("write beginning biographie")
st.write("First part in biographie : ", prefix)

generate = st.button("Generate le model")

# if train:
    
#     file_name = "data/biographie.txt"
#     # WikiFactory().build_biographie(file_name)
#     # biographie_df = pd.read_csv(
#     #     filename, encoding="utf-8", sep=";", usecols=["name", "biographie"]
#     # )
    
if generate:
    
    st.markdown(BiographieGenerator(model_name="124M", run_name='run1').generate_biographie(prefix=prefix))
    
#run_name="run1"
