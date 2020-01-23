import streamlit as st


def content():
    st.sidebar.title("About")
    st.info('"Les Quiromanciers" est un projet développé dans le cadre du cours de Traitement Automatique du Langage\
                Naturel (TALN) à l\'ESGI.')
    st.info('Retrouve le code sur Git ! '
            'https://github.com/Harisonm/Quiromanciers')
    st.balloons()

