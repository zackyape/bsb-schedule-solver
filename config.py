"""
config.py

Global configuration for BSB Schedule Solver.

Author  : Zacky Aji Pangestu
Version : 2.0.0
Python  : 3.12+
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

# ============================================================
# Application
# ============================================================

APP_NAME: str = "BSB Schedule Solver"
VERSION: str = "2.0.0"

# ============================================================
# Root Path
# ============================================================

ROOT_DIR: Path = Path(__file__).resolve().parent

# ============================================================
# File Configuration
# ============================================================


@dataclass(slots=True)
class FileConfig:
    """
    Input / Output file configuration.
    """

    input_excel: Path = ROOT_DIR / "Rekap_Jaga_Gudang_BSB_Juli_2026.xlsx"

    output_excel: Path = (
        ROOT_DIR / "Rekap_Jaga_Gudang_BSB_Juli_2026_Final.xlsx"
    )

    report_txt: Path = ROOT_DIR / "report.txt"

    report_csv: Path = ROOT_DIR / "report.csv"

    statistics_excel: Path = ROOT_DIR / "statistics.xlsx"


# ============================================================
# Excel Configuration
# ============================================================


@dataclass(slots=True)
class ExcelConfig:
    """
    Excel parser configuration.
    """

    auto_detect_sheet: bool = True

    sheet_name: str | None = None

    auto_detect_header: bool = True

    header_row: int = 4

    personnel_column: int = 1

    first_day_column: int = 2

    last_day_column: int = 32

    auto_detect_personnel: bool = True

    auto_detect_days: bool = True


# ============================================================
# Label Configuration
# ============================================================


@dataclass(slots=True)
class LabelConfig:
    """
    Assignment labels.
    """

    labels: tuple[str, ...] = (
        "A",
        "B",
        "C",
    )

    lock_values: set[str] = field(
        default_factory=lambda: {
            "A",
            "B",
            "C",
        }
    )

    empty_values: set = field(
        default_factory=lambda: {
            1,
            "1",
        }
    )


# ============================================================
# Personnel Configuration
# ============================================================


@dataclass(slots=True)
class PersonnelConfig:
    """
    Personnel settings.
    """

    ignored_personnel: set[str] = field(
        default_factory=lambda: {
            "ECOM",
        }
    )


# ============================================================
# Solver Configuration
# ============================================================


@dataclass(slots=True)
class SolverConfig:
    """
    Google OR-Tools CP-SAT configuration.
    """

    max_time_seconds: int = 300

    num_search_workers: int = 8

    random_seed: int = 12345

    log_search_progress: bool = False

    enumerate_all_solutions: bool = False


# ============================================================
# Constraint Configuration
# ============================================================


@dataclass(slots=True)
class ConstraintConfig:
    """
    Enable / Disable hard constraints.
    """

    enable_daily_abc: bool = True

    enable_locked_cells: bool = True

    enable_no_repeat: bool = True

    enable_no_abab: bool = True

    enable_no_acac: bool = True

    enable_no_bcbc: bool = True

    enable_single_label: bool = True

    enable_single_person: bool = True


# ============================================================
# Objective Configuration
# ============================================================


@dataclass(slots=True)
class ObjectiveConfig:
    """
    Soft constraints.
    """

    weekly_c_limit: int = 1

    enable_balance: bool = True

    enable_spread_c: bool = True

    enable_preferred_pattern: bool = True

    weight_weekly_c: int = 100

    weight_balance: int = 20

    weight_pattern: int = 5

    weight_spread_c: int = 10


# ============================================================
# Calendar Configuration
# ============================================================


@dataclass(slots=True)
class CalendarConfig:
    """
    Calendar weeks.
    """

    weeks: dict[int, range] = field(
        default_factory=lambda: {
            1: range(1, 6),
            2: range(6, 13),
            3: range(13, 20),
            4: range(20, 27),
            5: range(27, 32),
        }
    )


# ============================================================
# Report Configuration
# ============================================================


@dataclass(slots=True)
class ReportConfig:
    """
    Report settings.
    """

    generate_txt: bool = True

    generate_csv: bool = True

    generate_statistics: bool = True

    include_validation: bool = True


# ============================================================
# Debug Configuration
# ============================================================


@dataclass(slots=True)
class DebugConfig:
    """
    Debug settings.
    """

    enabled: bool = False

    print_solver_statistics: bool = False

    print_constraints: bool = False

    print_objectives: bool = False

    save_cp_model: bool = False


# ============================================================
# Global Config
# ============================================================


@dataclass(slots=True)
class AppConfig:
    """
    Root application configuration.
    """

    files: FileConfig = field(default_factory=FileConfig)

    excel: ExcelConfig = field(default_factory=ExcelConfig)

    labels: LabelConfig = field(default_factory=LabelConfig)

    personnel: PersonnelConfig = field(default_factory=PersonnelConfig)

    solver: SolverConfig = field(default_factory=SolverConfig)

    constraints: ConstraintConfig = field(
        default_factory=ConstraintConfig
    )

    objective: ObjectiveConfig = field(
        default_factory=ObjectiveConfig
    )

    calendar: CalendarConfig = field(
        default_factory=CalendarConfig
    )

    report: ReportConfig = field(
        default_factory=ReportConfig
    )

    debug: DebugConfig = field(
        default_factory=DebugConfig
    )


config = AppConfig()
