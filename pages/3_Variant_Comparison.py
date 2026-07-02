import streamlit as st
import plotly.express as px

from utils.session import *
from utils.sidebar import sidebar_filters
from utils.preprocessing import *
from utils.statistics import *

initialize()

st.title("Variant Comparison")

if not loaded():
    st.warning("Load experiments from Overview page.")
    st.stop()

exp = sidebar_filters()

latency = get_latency_df(exp)

if latency.empty:
    st.error("No latency logs found.")
    st.stop()


#####################################################
# Metric Selection
#####################################################

PREFERRED_METRICS = [
    "RTT_ms",
    "Processing_ms",
    "QueueDelay_ms",
    "Network_ms",
    "RenderDelay_ms",
    "MTP_ms",
    "Jitter_ms"
]

metrics = [m for m in PREFERRED_METRICS if m in latency.columns]

metric = st.sidebar.selectbox(
    "Metric",
    metrics,
    key="variant_metric"
)

#####################################################
# Protocol Selection
#####################################################

protocol = st.sidebar.selectbox(

    "Protocol",

    sorted(latency.Protocol.unique())

)

#####################################################
# Filter Protocol
#####################################################

df = latency[latency.Protocol == protocol]

#####################################################
# Chart
#####################################################

fig = px.bar(

    df.groupby("Variant")[metric]
      .mean()
      .reset_index(),

    x="Variant",

    y=metric,

    color="Variant",

    text_auto=".2f",

    title=f"{protocol} : Mean {metric}"

)

fig.update_layout(

    height=650,

    template="plotly_white"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

#####################################################
# Statistics
#####################################################

st.subheader("Statistics")

stats = (

    df.groupby("Variant")[metric]

    .describe()

)

st.dataframe(

    stats,

    use_container_width=True

)