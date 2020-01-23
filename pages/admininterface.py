import streamlit as st
import pandas as pd
from lesQuiromanciers.factory.WikiFactory import WikiFactory
from lesQuiromanciers.model.gpt2.BiographieGenerator import BiographieGenerator


def content():
    st.sidebar.title("Admin Interface")
    st.sidebar.info("Ici tu peux entraîner les modèles en fonction d'une liste de nom dont on va aller chercher la biographie")
    name_list = pd.DataFrame({
        'Label': ['Des biographies génériques'],
        'Filename': ['people.csv']
    })

    st.write(name_list)

    option = st.selectbox(
        'Which model do you want to train ?',
        name_list['Label'])
    generate_data = st.button("Fetch Data From Wikipedia")

    file_name_source = str("data/" + name_list[name_list['Label'] == option]['Filename'][0])
    file_name_destination = str("data/biographie" + option.replace(" ", "") + ".txt")
    model_name = option.replace(" ", "_")

    if generate_data:
        flag = WikiFactory().build_biographie(file_name_source, file_name_destination)
        st.write('You selected: ', option)

    traning = st.button("Fine Tune The Model")
    if traning:
        BiographieGenerator(model_name="124M", run_name=model_name).prepare_fine_tuning(file_name_destination)
