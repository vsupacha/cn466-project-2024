import streamlit as st
import pandas as pd
import os
import json

# Dynamically resolve the path
file_path = os.path.join(os.path.dirname(__file__), 'demo_data.txt')

# for mock-up only
with open(file_path, 'r') as file:
  raw_data = json.load(file)

search_id = st.text_input('Search by Data ID')

if not search_id or not search_id.isdigit() :
    st.write("There is no result")
else :
    df = pd.DataFrame(raw_data)
    try :
        st.write(df.loc[int(search_id)])
    except Exception as e:
        st.write("There is no result")
