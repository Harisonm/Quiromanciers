import streamlit as st
from lesQuiromanciers.factory.InstagramFactory import InstagramFactory
from lesQuiromanciers.model.instagram.InstagramClassification import (
    InstagramClassification,
)
import datetime as dt


def content():
    st.sidebar.title("Instagram Classification")
    st.sidebar.info("Voici comment on prépare le score instagram")
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
        try:
            instaData.download_data()
            df = instaData.dataframe_creation()
            st.info("Voici à quoi ressemble les données extraites d\'Instagram !")
            st.write(df)

            # Classer les utilisateurs selon Traveler Foody Musician
            instaClassifier = InstagramClassification(df, ['food', 'music', 'mountain'])
            classification = instaClassifier.result()
            st.info("On obtient ces scores générés à partir des données d\'Instagram")
            st.write(classification)

            st.info("Et ce graphique permettra à l'utilisateur de visualiser son profil instagrameur !")
            instaClassifier.print_classification()
        except:
            st.write('**Merci de rentrer un pseudo instagram qui existe !**')