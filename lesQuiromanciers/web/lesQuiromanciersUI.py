import streamlit as st
import pandas as pd
import numpy as np
import requests

file_name = st.text_input('give file name')
st.write('csv file name', file_name)

submit = st.button('submit new letters')
if submit:
    requests.get('http://0.0.0.0:5000/wiki/<file_name>').json()
    
# requests.get('http://0.0.0.0:5000/wiki/<file_name>', json=new_candidates)