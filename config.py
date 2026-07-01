"""
config.py

Global configuration for BSB Schedule Solver v2
"""

from dataclasses import dataclass, field
from pathlib import Path


# ==========================================================
# APP
# ==========================================================

APP_NAME = "BSB Schedule Solver"
VERSION = "2.0.0"


# ==========================================================
# PATHS
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent

INPUT_FILE = ROOT_DIR / "Rekap_Jaga_Gudang_BSB_Juli_2026.xlsx"
OUTPUT_FILE = ROOT_DIR / "Rekap_Jaga_Gudang_BSB_Juli_2026_Final.xlsx"

REPORT_TXT = ROOT_DIR / "report.txt"
REPORT_CSV = ROOT_DIR / "report.csv"
STATISTICS_FILE = ROOT_DIR / "statistics.xlsx"


# ==========================================================
# CONSTANTS
# ==========================================================

LABELS = ("A", "B", "C")

LOCK_VALUES = {"A", "B", "C"}

EMPTY_VALUES = {1, "1"}

IGNORE_PERSONNEL = {"ECOM"}


# ==========================================================
# EXCEL
# ==========================================================

@dataclass(slots=True)
class ExcelConfig:

    sheet_name: str = "Rekap Jaga Juli 2026"

    first_day_column: int = 2

    last_day_column: int = 32

    personnel_column: int = 1

    auto_detect_sheet: bool = True


# ==========================================================
# SOLVER
# ==========================================================

@dataclass(slots=True)
class SolverConfig:

    max_solver_time: int = 300

    num_workers: int = 8

    random_seed: int = 12345

    log_search_progress: bool = False


# ==========================================================
# HARD CONSTRAINTS
# ==========================================================

@dataclass(slots=True)
class ConstraintConfig:

    daily_abc: bool = True

    locked_cells: bool = True

    no_repeat: bool = True

    no_abab: bool = True

    no_acac: bool = True

    no_bcbc: bool = True

    one_label_per_person: bool = True

    one_person_per_label: bool = True


# ==========================================================
# SOFT CONSTRAINTS
# ==========================================================

@dataclass(slots=True)
class ObjectiveConfig:

    weekly_c_limit: int = 1

    balance_labels: bool = True

    spread_c: bool = True

    avoid_long_cycle: bool = True

    preferred_pattern: bool = True

    weight_weekly_c: int = 100

    weight_balance: int = 20

    weight_pattern: int = 5


# ==========================================================
# CALENDAR
# ==========================================================

@dataclass(slots=True)
class CalendarConfig:

    weeks: dict[int, range] = field(default_factory=lambda: {

        1: range(1, 6),

        2: range(6, 13),

        3: range(13, 20),

        4: range(20, 27),

        5: range(27, 32),

    })


# ==========================================================
# REPORT
# ==========================================================

@dataclass(slots=True)
class ReportConfig:

    generate_txt: bool = True

    generate_csv: bool = True

    generate_statistics: bool = True


# ==========================================================
# DEBUG
# ==========================================================

@dataclass(slots=True)
class DebugConfig:

    enabled: bool = False

    print_constraints: bool = False

    print_solver_stats: bool = False


# ==========================================================
# GLOBAL CONFIG
# ==========================================================

excel = ExcelConfig()

solver = SolverConfig()

constraints = ConstraintConfig()

objective = ObjectiveConfig()

calendar = CalendarConfig()

report = ReportConfig()

debug = DebugConfig()
