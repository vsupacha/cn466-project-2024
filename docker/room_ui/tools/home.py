import streamlit as st
import pandas as pd
import json
import os

# Dynamically resolve the path
file_path = os.path.join(os.path.dirname(__file__), 'demo_data.txt')

# for mock-up only
with open(file_path, 'r') as file:
  raw_data = json.load(file)

# Main UI
st.write('Data Monitor')

fetch_btn = st.button('Fetch Data')

df = pd.DataFrame(raw_data)

# for display only last 5 items afte click btn
if fetch_btn:
  last_5_items = df.tail(5)
  st.write(last_5_items)