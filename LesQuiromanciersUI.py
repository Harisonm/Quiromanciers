import streamlit as st
import pandas as pd
import numpy as np
import requests
from lesQuiromanciers.model.gpt2.BiographieGenerator import BiographieGenerator
from lesQuiromanciers.factory.InstagramFactory import InstagramFactory
from lesQuiromanciers.factory.WikiFactory import WikiFactory
# "Mirana Rakotonaina was born in 1995 in Madagascar. She is married to Manitra Ranaivoharison. The couple love Jesus."
seed = st.text_input('write beginning biographie')
st.write('First part in biographie : ', seed)

submit = st.button('submit new letters')
if submit:
    
    file_name = "data/biographie.txt"
    # WikiFactory().build_biographie(file_name)
    # biographie_df = pd.read_csv(
    #     filename, encoding="utf-8", sep=";", usecols=["name", "biographie"]
    # )
    
    BiographieGenerator(model_name="124M",file_name=file_name).generate_biographie(seed)
    
    st.text('This is some text.')