import streamlit as st
import pandas as pd

# Sidebar
st.sidebar.write('Settings:')
fetch_btn = st.sidebar.button('Fetch Data')


# Main UI
st.write('Data Monitor')

raw_data = [
  {
    "timestamp": "2024-11-13T08:00:00Z",
    "status": "open",
    "location": "422"
  },
  {
    "timestamp": "2024-11-14T08:00:00Z",
    "status": "open",
    "location": "422"
  },
  {
    "timestamp": "2024-11-15T08:00:00Z",
    "status": "close",
    "location": "422"
  },
  {
    "timestamp": "2024-11-16T08:00:00Z",
    "status": "open",
    "location": "422"
  },
  {
    "timestamp": "2024-11-17T08:00:00Z",
    "status": "close",
    "location": "422"
  },
  {
    "timestamp": "2024-11-18T08:00:00Z",
    "status": "open",
    "location": "422"
  },
  {
    "timestamp": "2024-11-19T08:00:00Z",
    "status": "open",
    "location": "422"
  },
  {
    "timestamp": "2024-11-20T08:00:00Z",
    "status": "close",
    "location": "422"
  }
]


df = pd.DataFrame(raw_data)


# for display only last 5 items afte click btn
if fetch_btn:
    last_5_items = df.tail(5)
    st.write(last_5_items)
