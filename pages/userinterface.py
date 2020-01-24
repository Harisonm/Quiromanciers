# Python 2/3 compatibility
from __future__ import print_function, division, unicode_literals, absolute_import
import streamlit as st
import pandas as pd
import re
import numpy as np
import requests
from io import BytesIO
from PIL import Image
from traceback import print_exc
from lesQuiromanciers.model.gpt2.BiographieGenerator import BiographieGenerator
from lesQuiromanciers.factory.InstagramFactory import InstagramFactory
from lesQuiromanciers.model.instagram.InstagramClassification import (
    InstagramClassification,
)
import datetime as dt
from lesQuiromanciers.factory.WikiFactory import WikiFactory
from streamlit.compatibility import setup_2_3_shims

def content():
    st.sidebar.header("User Interface")
    st.sidebar.info("Bienvenue sur l'application **Les Quiromanciers ** qui te permet de te générer une biographie \
                    fictive en fonction de ton profil Instagram ! ")
    st.sidebar.info("Rentre ton pseudo instagram et c'est parti !")
    pseudoIG = st.text_input(
        "Please enter your instagram pseudo. Example : guatemala_magica, jessieware, chef.etchebest, joshmeader22")
    classi = st.button("Generate")
    if classi:
        instaData = InstagramFactory(
            [
                pseudoIG
            ],
            dt.datetime(2019, 8, 1),
            dt.datetime(2019, 12, 31),
        )
        
        try:
            instaData.download_data()
            df = instaData.dataframe_creation()

            # Classer les utilisateurs selon Traveler et/ou Foody
            instaClassifier = InstagramClassification(df, ['food', 'music', 'mountain'])
            classification = instaClassifier.result()


            instaClassifier.print_classification()

            dict = {}
            dict['foody'] = classification['food'].values[0]
            dict['musician'] = classification['music'].values[0]
            dict['traveler'] = classification['mountain'].values[0]

            major_label = max(dict, key=dict.get)
            st.write('Congrats, you are ' + major_label)

            name_list = pd.DataFrame({
                'Label': ['foody', 'traveler', 'musician'],
                'model_name': ['run1', 'Explorer', 'Musician']
            })
            # Explorer Cooking_Expert
            model_name = name_list[name_list['Label'] == major_label]['model_name'].values[0]
            
            prefix = st.text_input("Write tailing about you to begin your biographie, example : Valentin was born in Madagascar. Valentin is " + major_label)
            generate = st.button("Predict")

            if generate:
                biographie = BiographieGenerator(model_name="124M", run_name=model_name, nsamples=1).generate_biographie(prefix=prefix)
                st.write(biographie)

        except:
            st.write("Write Instagram account existing")
            print_exc()


