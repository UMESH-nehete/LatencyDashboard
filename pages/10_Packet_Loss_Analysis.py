import streamlit as st
import pandas as pd

from utils.session import *
from utils.sidebar import sidebar_filters
from utils.preprocessing import *
from utils.loss_analysis import find_missing_packets

initialize()

st.title("Packet Loss Analysis")

if not loaded():
    st.warning("Load data from Overview.")
    st.stop()

experiments = sidebar_filters()

latency = get_latency_df(experiments)

packet = get_packet_df(experiments)

if latency.empty or packet.empty:
    st.error("Latency or Packet log missing.")
    st.stop()

protocols = sorted(packet.Protocol.unique())

summary = []

for protocol in protocols:

    p = packet[packet.Protocol == protocol]

    l = latency[latency.Protocol == protocol]

    missing = find_missing_packets(p, l)

    summary.append({

        "Protocol": protocol,

        "Packet Log": len(p),

        "Latency Log": len(l),

        "Missing": len(missing)

    })

    with st.expander(f"{protocol} Missing Packet Sequences"):

        if len(missing) == 0:

            st.success("No missing packets")

        else:

            st.write(missing)

summary_df = pd.DataFrame(summary)

st.subheader("Summary")

st.dataframe(summary_df, use_container_width=True)