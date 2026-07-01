"""
Optimizer Module untuk BSB Schedule Solver V2.1.
Mengelola pembuatan variabel, penerapan aturan (rules), fungsi objektif,
dan eksekusi solver Google OR-Tools CP-SAT.
"""

import time
from ortools.sat.python import cp_model

from config import LABELS
from models import WorkbookData, VariableStore, SolverResult
from rules import (
    LockedRule, OneLabelRule, DailyABCRule, NoRepeatRule, NoABABRule,
    WeeklyCRule, BalanceRule, SpreadCRule
)
from utils import timer


class ScheduleOptimizer:
    """Kelas utama untuk menjalankan CP-SAT Optimizer."""

    def __init__(self, data: WorkbookData, max_time_seconds: float = 60.0):
        """
        Inisialisasi Optimizer.

        Args:
            data (WorkbookData): Data lengkap yang telah diekstrak dari Excel.
            max_time_seconds (float): Batas maksimal waktu pencarian (dalam detik).
        """
        self.data = data
        self.max_time_seconds = max_time_seconds
        self.model = cp_model.CpModel()
        self.store = VariableStore(self.model)

    def solve(self) -> SolverResult:
        """
        Alur utama optimasi penjadwalan sesuai workflow SDD:
        Create Variables -> Apply Rules -> Collect Penalty -> Minimize -> Solve -> Return Result
        """
        start_time = time.perf_counter()

        with timer("Create Variables"):
            self._create_variables()

        with timer("Apply Hard Rules"):
            self._apply_hard_rules()

        with timer("Apply Soft Rules & Collect Penalty"):
            self._apply_soft_rules_and_minimize()

        with timer("Solve CP-SAT Model"):
            solver = cp_model.CpSolver()
            
            # Konfigurasi parameter solver
            solver.parameters.max_time_in_seconds = self.max_time_seconds
            solver.parameters.log_search_progress = True 
            solver.parameters.num_search_workers = 8  # Manfaatkan multi-core CPU

            status = solver.Solve(self.model)

        solve_time_seconds = time.perf_counter() - start_time

        # Ekstrak hasil jika solver menemukan solusi (Optimal atau Feasible)
        assignments = {}
        objective_val = 0.0

        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            objective_val = solver.ObjectiveValue()
            for person in self.data.people:
                assignments[person.name] = {}
                for day in self.data.schedules:
                    # Cari label (A/B/C) yang bernilai 1 (True) di hasil solver
                    for label in LABELS:
                        var = self.store.get(person.name, day.day_index, label)
                        if var is not None and solver.Value(var) == 1:
                            assignments[person.name][day.day_index] = label
                            break  # Berhenti mencari label lain berkat OneLabelRule

        return SolverResult(
            status=status,
            assignments=assignments,
            objective_value=objective_val,
            solve_time_seconds=solve_time_seconds
        )

    def _create_variables(self) -> None:
        """Membuat seluruh variabel boolean ruang pencarian (Person x Day x Label)."""
        for person in self.data.people:
            for day in self.data.schedules:
                for label in LABELS:
                    self.store.create(person.name, day.day_index, label)

    def _apply_hard_rules(self) -> None:
        """Menerapkan batasan operasional yang wajib dipenuhi (Hard Constraints)."""
        LockedRule.apply(self.model, self.store, self.data)
        OneLabelRule.apply(self.model, self.store, self.data)
        DailyABCRule.apply(self.model, self.store, self.data)
        NoRepeatRule.apply(self.model, self.store, self.data)
        NoABABRule.apply(self.model, self.store, self.data)

    def _apply_soft_rules_and_minimize(self) -> None:
        """Menerapkan batasan prioritas dan menekan akumulasi penalti serendah mungkin."""
        penalties = []
        
        penalties.extend(WeeklyCRule.apply(self.model, self.store, self.data))
        penalties.extend(BalanceRule.apply(self.model, self.store, self.data))
        penalties.extend(SpreadCRule.apply(self.model, self.store, self.data))
        
        if penalties:
            # Menginstruksikan solver mencari solusi dengan nilai penalti terkecil
            self.model.Minimize(sum(penalties))
          
