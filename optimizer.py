"""
optimizer.py
CP-SAT optimizer
"""
from ortools.sat.python import cp_model

from config import LABELS, solver
from constraints import DEFAULT_CONSTRAINTS
from objective import DEFAULT_OBJECTIVES
from models import SolverResult


class ScheduleOptimizer:

    def __init__(self, workbook):
        self.workbook = workbook
        self.model = cp_model.CpModel()
        self.variables = {}

    def _build_variables(self):
        for day in self.workbook.days:
            for person in day.personnel:
                for label in LABELS:
                    self.variables[(person, day.day, label)] = (
                        self.model.NewBoolVar(
                            f"{person}_{day.day}_{label}"
                        )
                    )

    def solve(self):
        self._build_variables()

        for c in DEFAULT_CONSTRAINTS:
            c.apply(
                self.model,
                self.variables,
                self.workbook,
            )

        penalties = []

        for obj in DEFAULT_OBJECTIVES:
            penalties.extend(
                obj.build(
                    self.model,
                    self.variables,
                    self.workbook,
                )
            )

        if penalties:
            self.model.Minimize(sum(penalties))

        cp = cp_model.CpSolver()
        cp.parameters.max_time_in_seconds = solver.max_solver_time
        cp.parameters.num_search_workers = solver.num_workers
        cp.parameters.random_seed = solver.random_seed
        cp.parameters.log_search_progress = solver.log_search_progress

        status = cp.Solve(self.model)

        if status not in (
            cp_model.OPTIMAL,
            cp_model.FEASIBLE,
        ):
            return SolverResult(
                solved=False,
                objective_value=0,
                assignments={},
                row_lookup={},
            )

        assignments = {}
        rows = {}

        for person in self.workbook.people.values():
            rows[person.name] = person.row

        for day in self.workbook.days:
            assignments[day.day] = {}
            for person in day.personnel:
                for label in LABELS:
                    if cp.Value(
                        self.variables[(person, day.day, label)]
                    ):
                        assignments[day.day][person] = label
                        break

        return SolverResult(
            solved=True,
            objective_value=cp.ObjectiveValue(),
            assignments=assignments,
            row_lookup=rows,
        )
        
