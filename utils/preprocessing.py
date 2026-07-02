import pandas as pd


###########################################################################
# Merge Latency Logs
###########################################################################

def get_latency_df(experiments):

    dfs = []

    for exp in experiments:

        if exp["log_type"] != "latency":
            continue

        df = exp["data"].copy()

        df["Protocol"] = exp["protocol"]
        df["Variant"] = exp["variant"]
        df["Date"] = exp["date"]
        df["File"] = exp["filename"]

        dfs.append(df)

    if len(dfs) == 0:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)


###########################################################################
# Merge Packet Logs
###########################################################################

def get_packet_df(experiments):

    dfs = []

    for exp in experiments:

        if exp["log_type"] != "packet":
            continue

        df = exp["data"].copy()

        df["Protocol"] = exp["protocol"]
        df["Variant"] = exp["variant"]
        df["Date"] = exp["date"]
        df["File"] = exp["filename"]

        dfs.append(df)

    if len(dfs) == 0:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)


###########################################################################
# Merge Queue Logs
###########################################################################

def get_queue_df(experiments):

    dfs = []

    for exp in experiments:

        if exp["log_type"] != "queue":
            continue

        df = exp["data"].copy()

        df["Protocol"] = exp["protocol"]
        df["Variant"] = exp["variant"]
        df["Date"] = exp["date"]
        df["File"] = exp["filename"]

        dfs.append(df)

    if len(dfs) == 0:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)