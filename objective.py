"""
objective.py

Soft objective plugins
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from ortools.sat.python import cp_model

from config import calendar, objective
from models import WorkbookData


# ==========================================================
# BASE CLASS
# ==========================================================

class Objective(ABC):

    name = "Objective"

    @abstractmethod
    def build(
        self,
        model: cp_model.CpModel,
        variables: dict,
        workbook: WorkbookData,
    ) -> List[cp_model.IntVar]:
        ...


# ==========================================================
# WEEKLY C
# ==========================================================

class WeeklyCObjective(Objective):

    name = "Weekly C"

    def build(
        self,
        model,
        variables,
        workbook,
    ):

        penalties = []

        for person in workbook.people.values():

            for week, days in calendar.weeks.items():

                c_vars = []

                for assign in person.assignments:

                    if assign.day in days:

                        c_vars.append(

                            variables[
                               
