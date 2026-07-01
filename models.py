"""
models.py

Data models for BSB Schedule Solver V2.1
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ortools.sat.python import cp_model


# ==========================================================
# ASSIGNMENT
# ==========================================================

@dataclass(slots=True)
class Assignment:
    """
    One duty assignment.
    """

    day: int

    label: Optional[str] = None

    locked: bool = False


# ==========================================================
# PERSON
# ==========================================================

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
    def history(self) -> list[Assignment]:

        return sorted(
            self.assignments,
            key=lambda x: x.day,
        )

    @property
    def total_assignment(self) -> int:

        return len(
            self.assignments
        )


# ==========================================================
# DAY SCHEDULE
# ==========================================================

@dataclass(slots=True)
class DaySchedule:
    """
    Schedule for one day.
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
        person: str,
    ) -> None:

        if person not in self.personnel:

            self.personnel.append(
                person
            )


# ==========================================================
# WORKBOOK
# ==========================================================

@dataclass(slots=True)
class WorkbookData:
    """
    Parsed workbook.
    """

    people: dict[str, Person]

    schedules: list[DaySchedule]

    row_lookup: dict[str, int]

    day_lookup: dict[int, int]

    @property
    def days(self) -> list[int]:

        return [
            schedule.day
            for schedule in self.schedules
        ]

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


# ==========================================================
# VARIABLE STORE
# ==========================================================

@dataclass(slots=True)
class VariableStore:
    """
    Store all CP-SAT variables.
    """

    assignments: dict[
        tuple[str, int, str],
        cp_model.IntVar,
    ] = field(default_factory=dict)

    def add(
        self,
        person: str,
        day: int,
        label: str,
        variable: cp_model.IntVar,
    ) -> None:

        self.assignments[
            (
                person,
                day,
                label,
            )
        ] = variable

    def get(
        self,
        person: str,
        day: int,
        label: str,
    ) -> cp_model.IntVar:

        return self.assignments[
            (
                person,
                day,
                label,
            )
        ]

    def labels(
        self,
        person: str,
        day: int,
        labels: tuple[str, ...],
    ) -> list[cp_model.IntVar]:

        return [

            self.get(
                person,
                day,
                label,
            )

            for label in labels

        ]

    def people_by_label(
        self,
        people: list[str],
        day: int,
        label: str,
    ) -> list[cp_model.IntVar]:

        return [

            self.get(
                person,
                day,
                label,
            )

            for person in people

        ]


# ==========================================================
# SOLVER RESULT
# ==========================================================

@dataclass(slots=True)
class SolverResult:
    """
    Result returned by optimizer.
    """

    solved: bool

    objective_value: float

    assignments: dict[
        int,
        dict[str, str],
    ]

    solver_status: str


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

    issues: list[
        ValidationIssue
    ] = field(
        default_factory=list
    )


# ==========================================================
# REPORT
# ==========================================================

@dataclass(slots=True)
class PersonStatistic:

    person: str

    a: int = 0

    b: int = 0

    c: int = 0

    weekly_c: dict[
        int,
        int,
    ] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class ReportData:

    statistics: list[
        PersonStatistic
    ]

    validation: ValidationResult
