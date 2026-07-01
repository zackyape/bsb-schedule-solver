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

                    self.x[(person, day.day, label)] = (
                        self.model.NewBoolVar(
                            f"{person}_{day.day}_{label}"
                        )
                    )

    # --------------------------------------------------

    def solve(self):

        builder = ConstraintBuilder(
            self.model,
            self.x
        )

        builder.daily_abc(
            self.active_people
        )

        builder.locked_cells(
            self.locked
        )

        builder.no_repeat(
            self.history
        )

        builder.no_abab(
            self.history
        )

        c_penalty = builder.weekly_c_limit(
            self.history,
            self.weeks
        )

        balance_penalty = builder.balance(
            self.history
        )

        self.model.Minimize(

            SOFT_WEIGHT_C
            * sum(c_penalty)

            +

            SOFT_WEIGHT_BALANCE
            * sum(balance_penalty)

        )

        solver = cp_model.CpSolver()

        solver.parameters.max_time_in_seconds = (
            MAX_SOLVER_TIME
        )

        solver.parameters.num_search_workers = (
            NUM_WORKERS
        )

        status = solver.Solve(self.model)

        if status not in (
            cp_model.OPTIMAL,
            cp_model.FEASIBLE,
        ):
            return None

        result = {}

        for day in self.days:

            result[day.day] = {}

            for person in day.active:

                for label in LABELS:

                    if solver.Value(

                        self.x[
                            (
                                person,
                                day.day,
                                label,
                            )
                        ]

                    ):

                        result[
                            day.day
                        ][person] = label

                        break

        return result
