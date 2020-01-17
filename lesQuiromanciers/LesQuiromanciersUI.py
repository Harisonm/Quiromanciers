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
BiographieGenerator(model_name="124M", run_name='run1').prepare_fine_tuning("data/biographie.txt")
if generate:
    
    st.markdown(BiographieGenerator(model_name="124M", run_name='run1').generate_biographie(prefix=prefix))
    
#run_name="run1"
