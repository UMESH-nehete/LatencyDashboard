import streamlit as st

from utils.session import *

from utils.loader import filter_experiments, experiment_table


def sidebar_filters():

    initialize()

    if not loaded():

        st.sidebar.warning("Load data from Overview page.")
        st.stop()

    experiments = st.session_state.experiments

    table = experiment_table(experiments)

    st.sidebar.title("Dashboard Filters")

    ###########################################################
    # Date
    ###########################################################

    dates = sorted(table["Date"].unique())

    selected_dates = st.sidebar.multiselect(
        "Date",
        dates,
        default=dates
    )

    ###########################################################
    # Protocol
    ###########################################################

    protocols = sorted(table["Protocol"].unique())

    selected_protocols = st.sidebar.multiselect(
        "Protocol",
        protocols,
        default=protocols
    )

    ###########################################################
    # Variant
    ###########################################################

    variants = sorted(table["Variant"].unique())

    selected_variants = st.sidebar.multiselect(
        "Variant",
        variants,
        default=variants
    )

    ###########################################################
    # Log Type
    ###########################################################

    log_types = sorted(table["Log Type"].unique())

    selected_logs = st.sidebar.multiselect(
        "Log Type",
        log_types,
        default=log_types
    )

    ###########################################################
    # Filter
    ###########################################################

    filtered = filter_experiments(
        experiments,
        protocols=selected_protocols,
        variants=selected_variants,
        dates=selected_dates,
        log_types=selected_logs
    )

    return filtered