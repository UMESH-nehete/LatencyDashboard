import streamlit as st

from utils.session import *
from utils.preprocessing import *
from utils.plotting import *
from utils.sidebar import sidebar_filters

initialize()

st.title("Protocol Comparison")

if not loaded():

    st.warning("Load experiments from Overview page.")

    st.stop()



exp = sidebar_filters()

latency = get_latency_df(exp)

if latency.empty:

    st.error("No latency logs found.")

    st.stop()

st.sidebar.header("Plot Options")

IGNORE_COLUMNS = [

    "T0_ms",
    "T1_ms",
    "T2_ms",
    "T3_ms",
    "T4_ms",
    "T5_ms",
    "T6_ms",

    "Frame",

    "Sequence",

    "Protocol",

    "Variant",

    "Date",

    "File"

]

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
    metrics
)

chart = st.sidebar.selectbox(

    "Chart",

    [

        "Bar",

        "Box",

        "Violin",

        "Histogram",

        "CDF",

        "Time Series",

        "Confidence Interval"

    ]

)

PLOTS = {

    "Bar": plot_bar,

    "Box": plot_box,

    "Violin": plot_violin,

    "Histogram": plot_histogram,

    "CDF": plot_cdf,

    "Time Series": plot_timeseries,

    "Confidence Interval": plot_confidence

}

fig = PLOTS[chart](latency, metric)

st.plotly_chart(

    fig,

    use_container_width=True

)

st.divider()

st.subheader("Statistics")

st.dataframe(

    latency.groupby("Protocol")[metric]

    .describe()

)