import streamlit as st
from dashboard import launch_dashboard

st.set_page_config(
    layout = 'wide',
    page_title = 'ClinicoAtlas',
    initial_sidebar_state="auto"
)

st.title('ClinicoAtlas')

launch_dashboard()

