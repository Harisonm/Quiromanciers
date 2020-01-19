import streamlit as st
import pandas as pd
import numpy as np
import requests
from lesQuiromanciers.model.gpt2.BiographieGenerator import BiographieGenerator
from lesQuiromanciers.factory.InstagramFactory import InstagramFactory
from lesQuiromanciers.factory.WikiFactory import WikiFactory

generate_data = st.button("Generate Data") # A Supprimer -> Test sur Kube
traning = st.button("traning Model")
generate = st.button("Generate Model")

file_name_source = "data/global_name_people.csv"
file_name_destination = "data/biographie_df.txt"

if generate_data:

    WikiFactory().build_biographie(file_name_source,file_name_destination)
    
    
if traning:
    
    BiographieGenerator(model_name="124M", run_name='run1').prepare_fine_tuning(file_name_destination)
    
prefix = st.text_input("write beginning biographie")
st.write("First part in biographie : ", prefix)
    
if generate:
    
    st.markdown(BiographieGenerator(model_name="124M", run_name='run1').generate_biographie(prefix=prefix))
    
