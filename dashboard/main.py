import streamlit as st
import os
import sys
from dashboard.views.view1 import display_view1

def main():
    st.title("Streamlit Dashboard")
    tab1 = st.tabs(["View 1", "View 2", "View 3"])

    with tab1:
        display_view1()

if __name__ == "__main__":
    main()