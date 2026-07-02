import streamlit as st
import pandas as pd
from utils.session import initialize, save

from utils.loader import (
    load_experiment,
    experiment_table,
    filter_experiments
)

initialize()

st.set_page_config(
    page_title="Overview",
    layout="wide"
)

st.title("📊 Network Latency Dashboard")

st.markdown("## Load Experiment Folder")

# -----------------------------
# Folder Selection
# -----------------------------

default_path = "/home/keerthana/Desktop/serverLogs"

folder = st.text_input(
    "Experiment Folder",
    value=default_path
)

col1, col2 = st.columns([1,5])

with col1:

    load = st.button(
        "Load Data",
        use_container_width=True
    )

# -----------------------------
# Load Data
# -----------------------------

if load:

    with st.spinner("Scanning folder..."):

        experiments = load_experiment(folder)

        save(
            folder,
             experiments,
                experiment_table(experiments)
            )

    st.success(f"Loaded {len(experiments)} log files.")


# -----------------------------
# Display if already loaded
# -----------------------------

from utils.session import loaded

if loaded():
    from utils.session import experiments, table

    experiments = experiments()

    table = table()

    st.divider()

    st.subheader("Summary")

    protocol_count = table["Protocol"].nunique()

    variant_count = table["Variant"].nunique()

    total_files = len(table)

    total_rows = table["Rows"].sum()

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Protocols",
        protocol_count
    )

    c2.metric(
        "Variants",
        variant_count
    )

    c3.metric(
        "CSV Files",
        total_files
    )

    c4.metric(
        "Total Rows",
        f"{total_rows:,}"
    )

    st.divider()

    st.subheader("Filters")

    col1,col2,col3 = st.columns(3)

    with col1:

        protocol = st.multiselect(
            "Protocol",
            sorted(table.Protocol.unique()),
            default=sorted(table.Protocol.unique())
        )

    with col2:

        variant = st.multiselect(
            "Variant",
            sorted(table.Variant.unique()),
            default=sorted(table.Variant.unique())
        )

    with col3:

        log_type = st.multiselect(
            "Log Type",
            sorted(table["Log Type"].unique()),
            default=sorted(table["Log Type"].unique())
        )

    filtered = filter_experiments(
        experiments,
        protocols=protocol,
        variants=variant,
        log_types=log_type
    )

    filtered_table = experiment_table(filtered)

    st.divider()

    st.subheader("Experiment Table")

    st.dataframe(
        filtered_table,
        use_container_width=True,
        height=600
    )

    st.download_button(
        "Download Table",
        filtered_table.to_csv(index=False),
        file_name="experiment_summary.csv",
        mime="text/csv"
    )