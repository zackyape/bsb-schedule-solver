"""
config.py
Global configuration for BSB Schedule Solver
"""

from pathlib import Path

# ==========================
# FILES
# ==========================

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "Rekap_Jaga_Gudang_BSB_Juli_2026.xlsx"
OUTPUT_FILE = BASE_DIR / "Rekap_Jaga_Gudang_BSB_Juli_2026_Final.xlsx"
REPORT_FILE = BASE_DIR / "report.txt"

# ==========================
# WORKBOOK
# ==========================

SHEET_NAME = "Rekap Jaga Juli 2026"

# ==========================
# PERSONNEL
# ==========================

PERSONNEL = [
    "HENDRO",
    "FARIKIN",
    "GILANG",
    "RISKY",
    "ZAKI",
    "YANUAR",
]

IGNORE_PERSONNEL = [
    "ECOM"
]

# ==========================
# ROWS
# ==========================

ROW_MAP = {
    "HENDRO": 5,
    "FARIKIN": 6,
    "GILANG": 7,
    "RISKY": 8,
    "ZAKI": 9,
    "YANUAR": 10,
    "ECOM": 11,
}

# ==========================
# DATE RANGE
# ==========================

FIRST_DAY_COLUMN = 2
LAST_DAY_COLUMN = 32

TOTAL_DAYS = 31

# ==========================
# LABELS
# ==========================

LABELS = [
    "A",
    "B",
    "C",
]

# ==========================
# CALENDAR WEEKS
# ==========================

WEEKS = {
    1: range(1, 6),
    2: range(6, 13),
    3: range(13, 20),
    4: range(20, 27),
    5: range(27, 32),
}

# ==========================
# SOLVER
# ==========================

MAX_SOLVER_TIME = 300

NUM_WORKERS = 8

# ==========================
# HARD CONSTRAINTS
# ==========================

ENABLE_DAILY_ABC = True
ENABLE_NO_REPEAT = True
ENABLE_NO_ABAB = True

# ==========================
# SOFT CONSTRAINTS
# ==========================

MAX_C_PER_WEEK = 1

SOFT_WEIGHT_C = 100
SOFT_WEIGHT_BALANCE = 20

# ==========================
# EXPORT
# ==========================

EXPORT_REPORT = True
EXPORT_STATISTICS = True

# ==========================
# DEBUG
# ==========================

DEBUG = False
