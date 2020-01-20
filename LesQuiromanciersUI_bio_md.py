import streamlit as st
import pandas as pd
import re
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import requests
from lesQuiromanciers.model.gpt2.BiographieGenerator import BiographieGenerator
from lesQuiromanciers.factory.InstagramFactory import InstagramFactory
from lesQuiromanciers.factory.WikiFactory import WikiFactory

def bio_style(bio):

    bio = re.sub("=", "#", bio)
    return bio


image = Image.open('/home/yasmine/PycharmProjects/Quiromanciers/data/sea_banner.jpeg')
st.image(image, use_column_width=True)

prefix = st.text_input("write beginning biographie")
st.write("First part in biographie : ", prefix)

generate = st.button("Generate le model")




if generate:

    """
    NAME : REMPLACER NAME PAR LE NOM DE TOTO

    BIOGRAPHIE : REMPLACER BIOGRAPHIE PAR LA BIOGRAPHIE GENEREE PAR LE MODELE 
    
    ET VIRER LE CODE ENTRE ///// ////

    """
    # ////////////////////////////////  A VIRER     //////////////////////////////////////////////////////
    biographie_df = pd.read_csv("/home/yasmine/PycharmProjects/Quiromanciers/data/biographie_df.csv",
                                encoding="utf-8", sep=";", usecols=["name", "biographie"])

    name = biographie_df.iloc[0,0]
    biographie = biographie_df.iloc[0,1]
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    st.write("# "+name)
    """
    REMPLACER URL PAR L URL DE LA PHOTO DE TOTO
    
    """

    url = "https://upload.wikimedia.org/wikipedia/commons/4/4a/Eminem_-_Concert_for_Valor_in_Washington%2C_D.C._Nov._11%2C_2014_%282%29_%28Cropped%29.jpg"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    st.image(img, width=200)
    st.write(bio_style(biographie))
    
#run_name="run1"
