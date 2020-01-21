# Python 2/3 compatibility
from __future__ import print_function, division, unicode_literals, absolute_import
import streamlit as st
import pandas as pd
import re
import numpy as np
import requests
from io import BytesIO
from PIL import Image
from lesQuiromanciers.model.gpt2.BiographieGenerator import BiographieGenerator
from lesQuiromanciers.factory.InstagramFactory import InstagramFactory
from lesQuiromanciers.factory.WikiFactory import WikiFactory
from streamlit.compatibility import setup_2_3_shims

def bio_style(bio):
    bio = re.sub("=", "#", bio)
    return bio


image = Image.open('data/sea_banner.jpeg')
file_name_source = "data/explorer.csv"
file_name_destination = "data/biographie_df.txt"

st.image(image, use_column_width=True)
setup_2_3_shims(globals())
generate_data = st.button("Generate Data") # A Supprimer -> Test sur Kube
traning = st.button("traning Model")

flag = False
if generate_data:
    flag = WikiFactory().build_biographie(file_name_source,file_name_destination)
    
if traning:
    BiographieGenerator(model_name="124M", run_name='run1').prepare_fine_tuning(file_name_destination)
    

name = st.text_input("Give your firstname folling your name, like example : Leonardo DICAPRIO")
prefix = st.text_input("Write tailing about you to begin your biographie, example : Mani was born in Madagascar.")

generate = st.button("Generate Model")
    
if generate:    
    biographie = BiographieGenerator(model_name="124M", run_name='run1').generate_biographie(prefix=prefix)
    st.write("# "+name)
    """
    REMPLACER URL PAR L URL DE LA PHOTO DE TOTO
    
    """
    url = "https://upload.wikimedia.org/wikipedia/commons/4/4a/Eminem_-_Concert_for_Valor_in_Washington%2C_D.C._Nov._11%2C_2014_%282%29_%28Cropped%29.jpg"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    st.image(img, width=200)
    st.write(bio_style(biographie))
    
  
