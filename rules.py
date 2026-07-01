"""
Rule Engine Module untuk BSB Schedule Solver V2.1.
Berisi semua definisi Hard Constraints dan Soft Constraints.
"""

from typing import List
from ortools.sat.python import cp_model

from config import (
    LABELS, EMPTY_CELL_MARKER, EXCLUDE_MARKER,
    PENALTY_WEEKLY_C, PENALTY_BALANCE, PENALTY_SPREAD_C, PENALTY_PREFERRED_PATTERN
)
from models import VariableStore, WorkbookData


# ==========================================
# HARD RULES (Wajib terpenuhi 100%)
# ==========================================

class LockedRule:
    """Mengunci sel sesuai template (A/B/C = Locked, Kosong = Libur, 1 = Bebas)."""
    @staticmethod
    def apply(model: cp_model.CpModel, store: VariableStore, data: WorkbookData) -> None:
        for assignment in data.assignments:
            p = assignment.person_name
            d = assignment.day_index
            val = assignment.label

            # Ambil semua variabel boolean untuk personel p di hari d
            vars_day = store.labels(p, d)
            if not vars_day:
                continue

            if assignment.is_locked and val in LABELS:
                # Kunci tepat ke label yang sudah ditentukan
                for lbl, var in zip(LABELS, vars_day):
                    if lbl == val:
                        model.Add(var == 1)
                    else:
                        model.Add(var == 0)
            elif val == EXCLUDE_MARKER:
                # Sel kosong = personel tidak jaga (semua variabel 0)
                for var in vars_day:
                    model.Add(var == 0)
            # Jika val == '1' (EMPTY_CELL_MARKER), biarkan solver yang menentukan


class OneLabelRule:
    """Setiap personel maksimal hanya mendapat 1 shift/label per hari (Tidak boleh dobel)."""
    @staticmethod
    def apply(model: cp_model.CpModel, store: VariableStore, data: WorkbookData) -> None:
        for person in data.people:
            for day in data.schedules:
                vars_day = store.labels(person.name, day.day_index)
                if vars_day:
                    model.AddAtMostOne(vars_day)


class DailyABCRule:
    """Setiap hari harus ada tepat 1 A, 1 B, dan 1 C di seluruh personel (One Person per Label)."""
    @staticmethod
    def apply(model: cp_model.CpModel, store: VariableStore, data: WorkbookData) -> None:
        for day in data.schedules:
            for label in LABELS:
                # Ambil semua variabel dari seluruh personel untuk hari dan label ini
                label_vars_across_people = store.day_label(day.day_index, label)
                if label_vars_across_people:
                    model.AddExactlyOne(label_vars_across_people)


class NoRepeatRule:
    """Mencegah personel mendapat shift yang persis sama di hari berturut-turut (AA, BB, CC)."""
    @staticmethod
    def apply(model: cp_model.CpModel, store: VariableStore, data: WorkbookData) -> None:
        for person in data.people:
            for label in LABELS:
                history = store.person_history(person.name, label)
                for i in range(len(history) - 1):
                    # var hari ini + var besok <= 1
                    model.Add(history[i] + history[i + 1] <= 1)


class NoABABRule:
    """Mencegah pola repetitif 4 hari seperti ABAB, ACAC, BCBC."""
    @staticmethod
    def apply(model: cp_model.CpModel, store: VariableStore, data: WorkbookData) -> None:
        for person in data.people:
            for l1 in LABELS:
                for l2 in LABELS:
                    if l1 == l2:
                        continue
                    
                    hist_l1 = store.person_history(person.name, l1)
                    hist_l2 = store.person_history(person.name, l2)
                    
                    # Cek setiap jendela 4 hari (d, d+1, d+2, d+3)
                    for i in range(len(hist_l1) - 3):
                        # Jika d=L1, d+1=L2, d+2=L1, maka d+3 tidak boleh L2
                        # Formula: L1(i) + L2(i+1) + L1(i+2) + L2(i+3) <= 3
                        model.Add(hist_l1[i] + hist_l2[i+1] + hist_l1[i+2] + hist_l2[i+3] <= 3)


# ==========================================
# SOFT RULES (Menghasilkan Penalti)
# ==========================================

class WeeklyCRule:
    """Soft: Penalti jika personel mendapat shift C lebih dari 1 kali dalam 7 hari."""
    @staticmethod
    def apply(model: cp_model.CpModel, store: VariableStore, data: WorkbookData) -> List[cp_model.IntVar]:
        penalties = []
        for person in data.people:
            hist_c = store.person_history(person.name, "C")
            # Iterasi per minggu (block of 7 days)
            for week_start in range(0, len(hist_c), 7):
                week_vars = hist_c[week_start:week_start + 7]
                if not week_vars:
                    continue
                
                sum_c = sum(week_vars)
                excess_c = model.NewIntVar(0, len(week_vars), f"excess_c_{person.name}_wk{week_start}")
                
                # excess_c >= sum_c - 1
                model.Add(excess_c >= sum_c - 1)
                # excess_c harus >= 0, CP-SAT IntVar sudah menjamin ini jika min bound 0
                
                penalty_term = model.NewIntVar(0, 1000, f"pen_wk_c_{person.name}_wk{week_start}")
                model.AddMultiplicationEquality(penalty_term, [excess_c, PENALTY_WEEKLY_C])
                penalties.append(penalty_term)
                
        return penalties


class BalanceRule:
    """Soft: Menjaga agar total shift tiap personel sebisa mungkin merata (mengurangi gap Max - Min)."""
    @staticmethod
    def apply(model: cp_model.CpModel, store: VariableStore, data: WorkbookData) -> List[cp_model.IntVar]:
        shift_counts = []
        for person in data.people:
            # Pengecualian jika personel adalah ECOM dan tidak ikut rotasi keseimbangan utama
            if person.is_ecom:
                continue
                
            person_total_vars = []
            for d in data.schedules:
                person_total_vars.extend(store.labels(person.name, d.day_index))
            
            total_shifts = sum(person_total_vars)
            shift_count_var = model.NewIntVar(0, 31, f"total_shifts_{person.name}")
            model.Add(shift_count_var == total_shifts)
            shift_counts.append(shift_count_var)

        if not shift_counts:
            return []

        max_shifts = model.NewIntVar(0, 31, "max_shifts")
        min_shifts = model.NewIntVar(0, 31, "min_shifts")
        
        model.AddMaxEquality(max_shifts, shift_counts)
        model.AddMinEquality(min_shifts, shift_counts)

        diff = model.NewIntVar(0, 31, "shifts_diff")
        model.Add(diff == max_shifts - min_shifts)

        penalty = model.NewIntVar(0, 1000, "pen_balance")
        model.AddMultiplicationEquality(penalty, [diff, PENALTY_BALANCE])
        
        return [penalty]


class SpreadCRule:
    """Soft: Penalti jika jarak antar shift C terlalu dekat (misal jarak 1 atau 2 hari bebas)."""
    @staticmethod
    def apply(model: cp_model.CpModel, store: VariableStore, data: WorkbookData) -> List[cp_model.IntVar]:
        penalties = []
        for person in data.people:
            hist_c = store.person_history(person.name, "C")
            
            # Cek jarak d+2 dan d+3 (karena d+1 sudah dilarang oleh NoRepeatRule - Hard Rule)
            for i in range(len(hist_c) - 3):
                # Jika C di hari i dan C di hari i+2 -> Terlalu dekat
                pen_bool_1 = model.NewBoolVar(f"pen_bool_c_dist2_{person.name}_d{i}")
                # Logika: Jika (hist_c[i] AND hist_c[i+2]) maka pen_bool_1 = True
                model.AddBoolOr([hist_c[i].Not(), hist_c[i+2].Not(), pen_bool_1])
                
                pen_val_1 = model.NewIntVar(0, PENALTY_SPREAD_C, f"pen_val_c_dist2_{person.name}_d{i}")
                model.AddMultiplicationEquality(pen_val_1, [pen_bool_1, PENALTY_SPREAD_C])
                penalties.append(pen_val_1)

                # Jika C di hari i dan C di hari i+3 -> Sedikit penalti
                pen_bool_2 = model.NewBoolVar(f"pen_bool_c_dist3_{person.name}_d{i}")
                model.AddBoolOr([hist_c[i].Not(), hist_c[i+3].Not(), pen_bool_2])
                
                pen_val_2 = model.NewIntVar(0, PENALTY_SPREAD_C // 2, f"pen_val_c_dist3_{person.name}_d{i}")
                model.AddMultiplicationEquality(pen_val_2, [pen_bool_2, PENALTY_SPREAD_C // 2])
                penalties.append(pen_val_2)
                
        return penalties
