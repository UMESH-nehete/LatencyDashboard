# config.py

from pathlib import Path

APP_NAME = "Network Latency Dashboard"

SUPPORTED_PROTOCOLS = [
    "TCP",
    "UDP",
    "WebRTC"
]

SUPPORTED_VARIANTS = [
    "baseline",
    "var1",
    "var2",
    "var3"
]

SUPPORTED_EXTENSIONS = [
    ".csv"
]

CACHE_TIME = 3600

DEFAULT_FIGURE_WIDTH = 1200
DEFAULT_FIGURE_HEIGHT = 600

ROOT = Path(".")