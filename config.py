"""
config.py

Global configuration for BSB Schedule Solver V2.1
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = "BSB Schedule Solver"
VERSION = "2.1.0"

ROOT_DIR = Path(__file__).resolve().parent


# ==========================================================
# FILE CONFIGURATION
# ==========================================================

@dataclass(slots=True)
class FilesConfig:
    """
    Project file locations.
    """

    input_excel: Path = (
        ROOT_DIR
        / "Rekap_Jaga_Gudang_BSB_Juli_2026.xlsx"
    )

    output_excel: Path = (
        ROOT_DIR
        / "Rekap_Jaga_Gudang_BSB_Juli_2026_Final.xlsx"
    )

    report_txt: Path = (
        ROOT_DIR
        / "report.txt"
    )

    report_csv: Path = (
        ROOT_DIR
        / "report.csv"
    )

    statistics_excel: Path = (
        ROOT_DIR
        / "statistics.xlsx"
    )


# ==========================================================
# EXCEL CONFIGURATION
# ==========================================================

@dataclass(slots=True)
class ExcelConfig:
    """
    Excel template configuration.
    """

    sheet_name: str = "Rekap Jaga Juli 2026"

    personnel_column: int = 1

    first_day_column: int = 2

    last_day_column: int = 32

    header_row: int = 4

    first_personnel_row: int = 5

    ignore_personnel: tuple[str, ...] = (
        "ECOM",
    )

    locked_values: tuple[str, ...] = (
        "A",
        "B",
        "C",
    )

    empty_values: tuple = (
        1,
        "1",
    )


# ==========================================================
# SOLVER CONFIGURATION
# ==========================================================

@dataclass(slots=True)
class SolverConfig:
    """
    Google OR-Tools configuration.
    """

    max_time_seconds: int = 300

    workers: int = 8

    random_seed: int = 12345

    log_search_progress: bool = False

    enumerate_all_solutions: bool = False


# ==========================================================
# RULE CONFIGURATION
# ==========================================================

@dataclass(slots=True)
class RuleConfig:
    """
    Scheduling rules.
    """

    labels: tuple[str, ...] = (
        "A",
        "B",
        "C",
    )

    weekly_c_limit: int = 1

    balance_weight: int = 20

    weekly_c_weight: int = 100

    spread_c_weight: int = 15

    preferred_pattern_weight: int = 5

    weeks: dict[int, range] = field(
        default_factory=lambda: {

            1: range(1, 6),

            2: range(6, 13),

            3: range(13, 20),

            4: range(20, 27),

            5: range(27, 32),

        }
    )


# ==========================================================
# REPORT CONFIGURATION
# ==========================================================

@dataclass(slots=True)
class ReportConfig:
    """
    Report generation.
    """

    generate_txt: bool = True

    generate_csv: bool = True

    generate_statistics: bool = True

    include_validation: bool = True

    include_solver_statistics: bool = True


# ==========================================================
# DEBUG CONFIGURATION
# ==========================================================

@dataclass(slots=True)
class DebugConfig:
    """
    Debug options.
    """

    enabled: bool = False

    print_solver_statistics: bool = False

    print_rule_statistics: bool = False

    save_cp_model: bool = False


# ==========================================================
# ROOT CONFIGURATION
# ==========================================================

@dataclass(slots=True)
class AppConfig:
    """
    Root configuration object.
    """

    files: FilesConfig = field(
        default_factory=FilesConfig
    )

    excel: ExcelConfig = field(
        default_factory=ExcelConfig
    )

    solver: SolverConfig = field(
        default_factory=SolverConfig
    )

    rules: RuleConfig = field(
        default_factory=RuleConfig
    )

    report: ReportConfig = field(
        default_factory=ReportConfig
    )

    debug: DebugConfig = field(
        default_factory=DebugConfig
    )


config = AppConfig()
