import streamlit as st

###########################################################################
# Initialize Session State
###########################################################################

def initialize():

    defaults = {

        "loaded": False,

        "folder": None,

        "experiments": None,

        "table": None,

        "filtered": None

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value

###########################################################################
# Store Loaded Data
###########################################################################

def save(folder, experiments, table):

    st.session_state.loaded = True

    st.session_state.folder = folder

    st.session_state.experiments = experiments

    st.session_state.table = table

###########################################################################
# Check
###########################################################################

def loaded():

    return st.session_state.loaded

###########################################################################
# Retrieve
###########################################################################

def experiments():

    return st.session_state.experiments

def table():

    return st.session_state.table