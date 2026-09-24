import os
from pathlib import Path

DB_PATH = Path(os.environ.get("PROPERTY_INTEL_DB", "data/property_intel.db"))
MATCH_WEIGHTS = {"address": 0.55, "geography": 0.15, "land": 0.12, "building": 0.08, "tenant": 0.10}
AUTO_MATCH = 0.93
REVIEW_MATCH = 0.75
