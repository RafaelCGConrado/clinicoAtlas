import streamlit as st
from dashboard import launch_dashboard

st.set_page_config(
    layout = 'wide',
    page_title = 'AKGrApp',
    initial_sidebar_state="auto"
)

st.title('AKGrApp')


launch_dashboard()

