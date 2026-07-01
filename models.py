"""
models.py

Data models for BSB Schedule Solver v2
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ==========================================================
# PERSON
# ==========================================================

@dataclass(slots=True)
class Person:
    """
    Represent one personnel.
    """

    name: str

    row: int

    assignments: List["Assignment"] = field(default_factory=list)


# ==========================================================
# ASSIGNMENT
# ==========================================================

@dataclass(slots=True)
class Assignment:
    """
    One assignment of one person.
    """

    day: int

    label: Optional[str]

    locked: bool


# ==========================================================
# DAY
# ==========================================================

@dataclass(slots=True)
class DaySchedule:
    """
    Schedule for one day.
    """

    day: int

    personnel: List[str] = field(default_factory=list)

    locked: Dict[str, str] = field(default_factory=dict)

    empty: List[str] = field(default_factory=list)


# ==========================================================
# WORKBOOK
# ==========================================================

@dataclass(slots=True)
class WorkbookData:
    """
    Parsed workbook.
    """

    people: Dict[str, Person]

    days: List[DaySchedule]


# ==========================================================
# SOLVER RESULT
# ==========================================================

@dataclass(slots=True)
class SolverResult:
    """
    Final schedule returned by optimizer.
    """

    solved: bool

    objective_value: float

    assignments: Dict[int, Dict[str, str]]

    statistics: Dict[str, Dict[str, int]]


# ==========================================================
# VALIDATION
# ==========================================================

@dataclass(slots=True)
class ValidationIssue:

    rule: str

    person: Optional[str]

    day: Optional[int]

    message: str


@dataclass(slots=True)
class ValidationResult:

    passed: bool

    issues: List[ValidationIssue] = field(default_factory=list)


# ==========================================================
# REPORT
# ==========================================================

@dataclass(slots=True)
class PersonStatistics:

    person: str

    total: int

    a_count: int

    b_count: int

    c_count: int

    weekly_c: Dict[int, int] = field(default_factory=dict)


@dataclass(slots=True)
class ReportData:

    statistics: List[PersonStatistics]

    validation: ValidationResult
