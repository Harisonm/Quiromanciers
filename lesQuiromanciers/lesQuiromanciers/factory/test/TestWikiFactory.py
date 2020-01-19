from lesQuiromanciers.factory.WikiFactory import WikiFactory
import pandas as pd
import csv
import os
import datetime as dt
import re
def clean_data(words):
    """
    clean_data [summary]
    
    Args:
        words ([type]): [description]
    
    Returns:
        [type]: [description]
    """
    words = str(words)
    words = re.sub(r'\(.*?\)', '', words)
    words = re.sub(r'\[.*?\]', '', words)
    return words

def tag_name(words):
    """
    tag_name [summary]
    
    Args:
        words ([type]): [description]
    
    Returns:
        [type]: [description]
    """
    name = words[0]
    print(name)
    print(type(name))
    names = name.split(' ')
    bio = words[1]
    if ' , known ' in bio[0:50]:
        bio = re.sub('^.* , known ' , '#name , known ', bio)
    if ' is ' in bio[0:50]:
        bio = re.sub('^.* is ' , '#name is ', bio)
    if ' was ' in bio[0:50]:
        bio = re.sub('^.* was ' , '#name was ', bio)
    bio = bio.replace(name, '#name')
    for n in names:
        bio = bio.replace(n, '#name')
    return bio
    
if __name__ == "__main__":
    
    WikiFactory().build_biographie("data/biographie_df.csv")