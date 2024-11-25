import streamlit as st
import pandas as pd
import json

# Sidebar
search_page = st.Page("tools/search.py", title="Search Data", icon=":material/search:")
edit_page = st.Page("tools/edit.py", title="Edit Data", icon=":material/edit:")
monitor_page = st.Page("tools/home.py", title="Monitor", icon=":material/home:")

pg = st.navigation([monitor_page, search_page, edit_page])
pg.run()
