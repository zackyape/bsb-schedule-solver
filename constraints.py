"""
constraints.py

Hard constraint plugins for BSB Schedule Solver v2
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List

from ortools.sat.python import cp_model

from models import WorkbookData


# ==========================================================
# BASE CLASS
# ==========================================================

class Constraint(ABC):

    name: str = "Constraint"

    @abstractmethod
    def apply(
        self,
        model: cp_model.CpModel,
        variables: dict,
        workbook: WorkbookData,
    ) -> None:
        pass


# ==========================================================
# DAILY ABC
# ==========================================================

class DailyABCConstraint(Constraint):

    name = "DailyABC"

    def apply(
        self,
        model,
        variables,
        workbook,
    ):

        for day in workbook.days:

            people = day.personnel

            for label in ("A", "B", "C"):

                model.Add(

                    sum(

                        variables[(p, day.day, label)]

                        for p in people

                    ) == 1

                )

            for person in people:

                model.Add(

                    sum(

                        variables[
                            (person, day.day, l)
                        ]

                        for l in ("A", "B", "C")

                    ) == 1

                )


# ==========================================================
# LOCKED CELL
# ==========================================================

class LockedConstraint(Constraint):

    name = "Locked"

    def apply(
        self,
        model,
        variables,
        workbook,
    ):

        for day in workbook.days:

            for person, label in day.locked.items():

                model.Add(

                    variables[
                        (person, day.day, label)
                    ]

                    == 1

                )


# ==========================================================
# NO REPEAT
# ==========================================================

class NoRepeatConstraint(Constraint):

    name = "NoRepeat"

    def apply(
        self,
        model,
        variables,
        workbook,
    ):

        for person in workbook.people.values():

            assigns = sorted(
                person.assignments,
                key=lambda a: a.day,
            )

            for i in range(len(assigns) - 1):

                d1 = assigns[i].day
                d2 = assigns[i + 1].day

                for label in ("A", "B", "C"):

                    model.Add(

                        variables[
                            (person.name, d1, label)
                        ]

                        +

                        variables[
                            (person.name, d2, label)
                        ]

                        <= 1

                    )


# ==========================================================
# NO ABAB
# ==========================================================

class NoABABConstraint(Constraint):

    BAD = [

        ("A", "B"),
        ("B", "A"),

        ("A", "C"),
        ("C", "A"),

        ("B", "C"),
        ("C", "B"),

    ]

    name = "NoABAB"

    def apply(
        self,
        model,
        variables,
        workbook,
    ):

        for person in workbook.people.values():

            assigns = sorted(
                person.assignments,
                key=lambda a: a.day,
            )

            if len(assigns) < 4:
                continue

            for i in range(len(assigns) - 3):

                d1 = assigns[i].day
                d2 = assigns[i + 1].day
                d3 = assigns[i + 2].day
                d4 = assigns[i + 3].day

                for a, b in self.BAD:

                    model.Add(

                        variables[
                            (person.name, d1, a)
                        ]

                        +

                        variables[
                            (person.name, d2, b)
                        ]

                        +

                        variables[
                            (person.name, d3, a)
                        ]

                        +

                        variables[
                            (person.name, d4, b)
                        ]

                        <= 3

                    )


# ==========================================================
# REGISTRY
# ==========================================================

DEFAULT_CONSTRAINTS: List[Constraint] = [

    DailyABCConstraint(),

    LockedConstraint(),

    NoRepeatConstraint(),

    NoABABConstraint(),

]
