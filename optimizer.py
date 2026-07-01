"""
optimizer.py
"""

from ortools.sat.python import cp_model

from constraints import ConstraintBuilder
from config import (
    LABELS,
    MAX_SOLVER_TIME,
    NUM_WORKERS,
    SOFT_WEIGHT_C,
    SOFT_WEIGHT_BALANCE,
)


class ScheduleOptimizer:

    def __init__(self, days, history, locked, weeks):

        self.days = days
        self.history = history
        self.locked = locked
        self.weeks = weeks

        self.model = cp_model.CpModel()

        self.x = {}

        self.active_people = {}

        self._build_variables()

    # --------------------------------------------------

    def _build_variables(self):

        for day in self.days:

            people = day.active

            self.active_people[day.day] = people

            for person in people:

                for label in LABELS:

                    self.x[(person, day.day
