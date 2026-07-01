"""
models.py

Data models for BSB Schedule Solver.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# ============================================================
# Assignment
# ============================================================

@dataclass(slots=True)
class Assignment:
    """
    One duty assignment.
    """

    day: int

    label: Optional[str] = None

    locked: bool = False


# ============================================================
# Person
# ============================================================

@dataclass(slots=True)
class Person:
    """
    One personnel.
    """

    name: str

    row: int

    assignments: list[Assignment] = field(
        default_factory=list
    )

    def add_assignment(
        self,
        assignment: Assignment,
    ) -> None:

        self.assignments.append(
            assignment
        )

    @property
    def total_assignment(self) -> int:

        return len(
            self.assignments
        )


# ============================================================
# DaySchedule
# ============================================================

@dataclass(slots=True)
class DaySchedule:
    """
    Schedule of one day.
    """

    day: int

    personnel: list[str] = field(
        default_factory=list
    )

    locked: dict[str, str] = field(
        default_factory=dict
    )

    empty: list[str] = field(
        default_factory=list
    )

    def add_person(
        self,
        name: str,
    ) -> None:

        if name not in self.personnel:

            self.personnel.append(
                name
            )

    @property
    def total_personnel(self) -> int:

        return len(
            self.personnel
        )


# ============================================================
# WorkbookData
# ============================================================

@dataclass(slots=True)
class WorkbookData:
    """
    Parsed workbook.
    """

    people: dict[str, Person]

    schedules: list[DaySchedule]

    @property
    def total_people(self) -> int:

        return len(
            self.people
        )

    @property
    def total_days(self) -> int:

        return len(
            self.schedules
        )


# ============================================================
# SolverResult
# ============================================================

@dataclass(slots=True)
class SolverResult:
    """
    Solver output.
    """

    solved: bool

    objective: float

    assignments: dict[int, dict[str, str]]

    row_lookup: dict[str, int]

    solver_status: str = ""


# ============================================================
# Validation
# ============================================================

@dataclass(slots=True)
class ValidationIssue:

    rule: str

    person: str | None

    day: int | None

    message: str


@dataclass(slots=True)
class ValidationResult:

    passed: bool

    issues: list[ValidationIssue] = field(
        default_factory=list
    )

    @property
    def total_issue(self) -> int:

        return len(
            self.issues
        )


# ============================================================
# Statistics
# ============================================================

@dataclass(slots=True)
class PersonStatistic:

    person: str

    a: int = 0

    b: int = 0

    c: int = 0

    weekly_c: dict[int, int] = field(
        default_factory=dict
    )

    @property
    def total(self) -> int:

        return self.a + self.b + self.c


@dataclass(slots=True)
class ReportData:

    statistics: list[PersonStatistic]

    validation: ValidationResult
