import pandas as pd


def find_missing_packets(packet_df, latency_df):
    """
    Returns packet sequence numbers that exist in packet_log
    but not in latency_log.
    """

    if packet_df.empty or latency_df.empty:
        return []

    # -------- Detect sequence column --------

    packet_seq = None
    latency_seq = None

    for c in packet_df.columns:
        if c.lower() in ["seq", "sequence", "packet_seq"]:
            packet_seq = c
            break

    for c in latency_df.columns:
        if c.lower() in ["seq", "sequence", "packet_seq"]:
            latency_seq = c
            break

    if packet_seq is None:
        raise ValueError("Sequence column not found in packet log.")

    if latency_seq is None:
        raise ValueError("Sequence column not found in latency log.")

    packet_sequences = set(packet_df[packet_seq].dropna().astype(int))

    latency_sequences = set(latency_df[latency_seq].dropna().astype(int))

    missing = sorted(packet_sequences - latency_sequences)

    return missing