from pathlib import Path
import pandas as pd
import streamlit as st
import os

##########################################################################
# Supported log names
##########################################################################

LOG_TYPES = {
    "latency": "latency_log",
    "packet": "packet_log",
    "queue": "queue_log"
}

##########################################################################
# Detect Protocol
##########################################################################

def detect_protocol(path: Path):

    parts = [p.lower() for p in path.parts]

    if "tcp" in parts:
        return "TCP"

    if "udp" in parts:
        return "UDP"

    if "webrtc" in parts:
        return "WebRTC"

    return "Unknown"

##########################################################################
# Detect Variant
##########################################################################

def detect_variant(path: Path):

    parts = [p.lower() for p in path.parts]

    variants = [
        "baseline",
        "var1",
        "var2",
        "var3",
        "var4",
        "var5"
    ]

    for v in variants:
        if v in parts:
            return v

    return "Unknown"

##########################################################################
# Detect Experiment Date
##########################################################################

def detect_date(path: Path):

    for part in path.parts:

        p = part.upper()

        if "JUNE" in p:
            return part

        if "MAY" in p:
            return part

        if "APRIL" in p:
            return part

    return "Unknown"

##########################################################################
# Detect Log Type
##########################################################################

def detect_log_type(filename):

    filename = filename.lower()

    for key, value in LOG_TYPES.items():

        if value in filename:

            return key

    return "unknown"

##########################################################################
# Scan Folder
##########################################################################

def scan_folder(folder):

    folder = Path(folder)

    csv_files = list(folder.rglob("*.csv"))

    return sorted(csv_files)

##########################################################################
# Read CSV safely
##########################################################################

def read_csv(file):

    try:

        df = pd.read_csv(file)

        return df

    except Exception as e:

        st.error(f"Cannot load {file}")

        st.exception(e)

        return None

##########################################################################
# Load All Data
##########################################################################

@st.cache_data(show_spinner=True)

def load_experiment(folder):

    files = scan_folder(folder)

    experiments = []

    for file in files:

        df = read_csv(file)

        if df is None:
            continue

        info = {

            "path": str(file),

            "filename": file.name,

            "protocol": detect_protocol(file),

            "variant": detect_variant(file),

            "date": detect_date(file),

            "log_type": detect_log_type(file.name),

            "data": df

        }

        experiments.append(info)

    return experiments

##########################################################################
# Convert to Summary DataFrame
##########################################################################

def experiment_table(experiments):

    rows = []

    for exp in experiments:

        rows.append({

            "Protocol": exp["protocol"],

            "Variant": exp["variant"],

            "Date": exp["date"],

            "Log Type": exp["log_type"],

            "Rows": len(exp["data"]),

            "File": exp["filename"]

        })

    return pd.DataFrame(rows)

##########################################################################
# Filter
##########################################################################

def filter_experiments(
        experiments,
        protocols=None,
        variants=None,
        dates=None,
        log_types=None
):

    output = []

    for exp in experiments:

        if protocols and exp["protocol"] not in protocols:
            continue

        if variants and exp["variant"] not in variants:
            continue

        if dates and exp["date"] not in dates:
            continue

        if log_types and exp["log_type"] not in log_types:
            continue

        output.append(exp)

    return output

##########################################################################
# Merge Same Log Type
##########################################################################

def merge_logs(experiments, log_type):

    dfs = []

    for exp in experiments:

        if exp["log_type"] == log_type:

            temp = exp["data"].copy()

            temp["Protocol"] = exp["protocol"]

            temp["Variant"] = exp["variant"]

            temp["Date"] = exp["date"]

            temp["File"] = exp["filename"]

            dfs.append(temp)

    if len(dfs) == 0:

        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)