"""
Configuration settings for SYSTEMSEM data extraction
"""

import os
from pathlib import Path

# SYSTEMSEM project path - UPDATE THIS TO YOUR SYSTEMSEM LOCATION
SYSTEMSEM_PATH = "/path/to/your/SYSTEMSEM"  # CHANGE THIS!

# Output directory
OUTPUT_DIR = Path("output")

# Key data paths within SYSTEMSEM
DATA_PATHS = {
    "correlations": "analyses/02_concreteness_semantics/data/wiki/mean_cluster_corrs",
    "language_metrics": "analyses/04_predicting_semantic_sim/data/lang_distance_metrics",
    "swadesh": "analyses/03_swadesh/data",
}

# File patterns to extract
FILE_PATTERNS = {
    "pairwise_correlations": "*pairwise_semantics_correlations_*.csv",
    "language_distance": "*language_distance*.csv",
    "swadesh_correlations": "*swadesh_correlations*.csv",
}

# Language codes mapping (ETS to standard codes)
LANGUAGE_MAPPING = {
    "ARA": "ar", "BEN": "bn", "BUL": "bg", "CHI": "zh", "DUT": "nl",
    "ENG": "en", "FAS": "fa", "FRE": "fr", "GER": "de", "GRE": "el",
    "GUJ": "gu", "HIN": "hi", "IBO": "ig", "IND": "id", "ITA": "it",
    "JPN": "ja", "KAN": "kn", "KOR": "ko", "MAL": "ml", "MAR": "mr",
    "NEP": "ne", "PAN": "pa", "POL": "pl", "POR": "pt", "RUM": "ro",
    "RUS": "ru", "SPA": "es", "TAM": "ta", "TEL": "te", "TGL": "tl",
    "THA": "th", "TUR": "tr", "URD": "ur", "VIE": "vi", "YOR": "yo"
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": OUTPUT_DIR / "extraction_log.txt"
}