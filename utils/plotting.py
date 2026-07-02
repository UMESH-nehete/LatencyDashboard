import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ---------------------------------------------------------
# Common Layout
# ---------------------------------------------------------

def apply_layout(fig, title):

    fig.update_layout(
        title=title,
        template="plotly_white",
        height=650,
        font=dict(size=16),
        legend_title="",
        margin=dict(
            l=30,
            r=30,
            t=60,
            b=30
        )
    )

    return fig


# ---------------------------------------------------------
# Bar Plot
# ---------------------------------------------------------

def plot_bar(df, metric, groupby="Protocol"):

    stats = (

        df.groupby(groupby)[metric]

        .mean()

        .reset_index()

    )

    fig = px.bar(

        stats,

        x=groupby,

        y=metric,

        color=groupby,

        text_auto=".2f"

    )

    return apply_layout(
        fig,
        f"Mean {metric}"
    )


# ---------------------------------------------------------
# Box Plot
# ---------------------------------------------------------

def plot_box(df, metric, groupby="Protocol"):

    fig = px.box(

        df,

        x=groupby,

        y=metric,

        color=groupby,

        points="outliers"

    )

    return apply_layout(
        fig,
        f"{metric} Distribution"
    )


# ---------------------------------------------------------
# Violin Plot
# ---------------------------------------------------------

def plot_violin(df, metric, groupby="Protocol"):

    fig = px.violin(

        df,

        x=groupby,

        y=metric,

        color=groupby,

        box=True

    )

    return apply_layout(
        fig,
        f"{metric} Distribution"
    )


# ---------------------------------------------------------
# Histogram
# ---------------------------------------------------------

def plot_histogram(df, metric):

    fig = px.histogram(

        df,

        x=metric,

        color="Protocol",

        marginal="box",

        barmode="overlay"

    )

    return apply_layout(
        fig,
        f"{metric} Histogram"
    )


# ---------------------------------------------------------
# Time Series
# ---------------------------------------------------------

def plot_timeseries(df, metric):

    fig = px.line(

        df,

        y=metric,

        color="Protocol"

    )

    return apply_layout(
        fig,
        f"{metric} vs Sample"
    )


# ---------------------------------------------------------
# CDF
# ---------------------------------------------------------

def plot_cdf(df, metric):

    fig = go.Figure()

    for protocol in sorted(df.Protocol.unique()):

        values = (

            df[df.Protocol == protocol][metric]

            .dropna()

            .sort_values()

            .values

        )

        y = np.arange(1, len(values)+1)/len(values)

        fig.add_trace(

            go.Scatter(

                x=values,

                y=y,

                mode="lines",

                name=protocol

            )

        )

    return apply_layout(
        fig,
        f"CDF : {metric}"
    )


# ---------------------------------------------------------
# Correlation
# ---------------------------------------------------------

def plot_heatmap(df):

    numeric = df.select_dtypes(include="number")

    corr = numeric.corr()

    fig = px.imshow(

        corr,

        text_auto=".2f",

        color_continuous_scale="RdBu"

    )

    return apply_layout(
        fig,
        "Correlation Matrix"
    )


# ---------------------------------------------------------
# Confidence Interval Plot
# ---------------------------------------------------------

def plot_confidence(df, metric, groupby="Protocol"):

    stats = (

        df.groupby(groupby)[metric]

        .agg(["mean","std","count"])

        .reset_index()

    )

    stats["ci"] = 1.96 * stats["std"] / np.sqrt(stats["count"])

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=stats[groupby],

            y=stats["mean"],

            error_y=dict(

                type="data",

                array=stats["ci"]

            )

        )

    )

    return apply_layout(
        fig,
        f"{metric} (95% CI)"
    )


# ---------------------------------------------------------
# Scatter
# ---------------------------------------------------------

def plot_scatter(df, x, y):

    fig = px.scatter(

        df,

        x=x,

        y=y,

        color="Protocol"

    )

    return apply_layout(
        fig,
        f"{y} vs {x}"
    )