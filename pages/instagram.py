import streamlit as st
from lesQuiromanciers.factory.InstagramFactory import InstagramFactory
from lesQuiromanciers.model.instagram.InstagramClassification import (
    InstagramClassification,
)
import datetime as dt

def content():
    st.sidebar.title("Instagram Classification")
    pseudoIG = st.text_input("Please enter your instagram pseudo. Example : guatemala_magica, jessieware, chef.etchebest, joshmeader22")
    classi = st.button("Tell me who am I")
    if classi:
        instaData = InstagramFactory(
            [
                pseudoIG
            ],
            dt.datetime(2019, 8, 1),
            dt.datetime(2019, 12, 31),
        )
        instaData.download_data()
        df = instaData.dataframe_creation()
        st.write(df)

        # Classer les utilisateurs selon Traveler et/ou Foody
        instaClassifier = InstagramClassification(df, ['food', 'music', 'mountain'])
        classification = instaClassifier.result()
        st.write(classification)

        instaClassifier.print_classification()