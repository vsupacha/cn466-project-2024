import streamlit as st
import pandas as pd
import os
import json

# Dynamically resolve the path
file_path = os.path.join(os.path.dirname(__file__), 'demo_data.txt')

# for mock-up only
with open(file_path, 'r') as file:
  raw_data = json.load(file)

df = pd.DataFrame(raw_data)

st.data_editor(df)
