import streamlit as st
import pandas as pd
from lesQuiromanciers.factory.WikiFactory import WikiFactory
from lesQuiromanciers.model.gpt2.BiographieGenerator import BiographieGenerator
import re

def content():
    st.sidebar.title("Biography")

    name_list = pd.DataFrame({
        'Label': ['Cooking Expert', 'Explorer', 'Musician'],
        'Filename': ['cooking_expert.csv', 'explorer.csv', 'musician.csv']
    })

    st.write(name_list)

    option = st.selectbox(
        'Which model do you want to train ?',
        name_list['Label'])
    generate_data = st.button("Fetch Data From Wikipedia")

    # file_name_source = "data/" + name_list[name_list['Label'] == option]['Filename']
    file_name_source = "data/people_test.csv"
    file_name_destination = "data/biographie" + option.replace(" ","") + ".txt"
    if generate_data:
        flag = WikiFactory().build_biographie(file_name_source,file_name_destination)
        st.write('You selected: ', option)

    traning = st.button("Fine Tune The Model")
    if traning:
        BiographieGenerator(model_name="124M", run_name='run1').prepare_fine_tuning(file_name_destination)

    name = st.text_input("Give your firstname folling your name, like example : Leonardo DICAPRIO")
    prefix = st.text_input("Write tailing about you to begin your biographie, example : Mani was born in Madagascar.")

    generate = st.button("Predict")

    if generate:
        biographie = BiographieGenerator(model_name="124M", run_name='run1').generate_biographie(prefix=prefix)
        st.write(biographie)
        # st.write("# "+name)
        # st.write(bio_style(str(biographie)))


def bio_style(bio):
    bio = re.sub("=", "#", bio)
    return bio

