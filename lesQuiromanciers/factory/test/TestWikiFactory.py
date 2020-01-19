from lesQuiromanciers.factory.WikiFactory import WikiFactory
import pandas as pd
import csv
import os
import datetime as dt
import re
    
if __name__ == "__main__":
    
    WikiFactory().build_biographie("data/people_test.csv","data/biographie_df.txt")