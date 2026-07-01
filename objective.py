"""
objective.py
Soft objective plugins for BSB Schedule Solver v2
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from ortools.sat.python import cp_model

from config import calendar, objective
from models import WorkbookData


class Objective(ABC):
    name = "Objective"

    @abstractmethod
    def build(
        self,
        model: cp_model.CpModel,
        variables: dict,
        workbook: WorkbookData,
    ) -> list:
        ...


class WeeklyCObjective(Objective):
    name = "WeeklyC"

    def build(self, model, variables, workbook):
        penalties = []

        for person in workbook.people.values():
            for week, days in calendar.weeks.items():
                c_vars = [
                    variables[(person.name, a.day, "C")]
                    for a in person.assignments
                    if a.day in days
                ]

                if not c_vars:
                    continue

                extra = model.NewIntVar(
                    0,
                    10,
                    f"C_{person.name}_{week}",
                )

                model.Add(
                    extra >= sum(c_vars) - objective.weekly_c_limit
                )

                penalties.append(
                    objective.weight_weekly_c * extra
                )

        return penalties


class BalanceObjective(Objective):
    name = "Balance"

    def build(self, model, variables, workbook):
        penalties = []

        for person in workbook.people.values():
            total = len(person.assignments)
            target = total // 3

            for label in ("A", "B", "C"):

                count = model.NewIntVar(
                    0,
                    total,
                    f"{person.name}_{label}",
                )

                model.Add(
                    count
                    ==
                    sum(
                        variables[(person.name, a.day, label)]
                        for a in person.assignments
                    )
                )

                diff = model.NewIntVar(
                    0,
                    total,
                    f"DIFF_{person.name}_{label}",
                )

                model.AddAbsEquality(
                    diff,
                    count - target,
                )

                penalties.append(
                    objective.weight_balance * diff
                )

        return penalties


DEFAULT_OBJECTIVES = [
    WeeklyCObjective(),
    BalanceObjective(),
]
