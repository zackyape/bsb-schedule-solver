"""
Data models untuk BSB Schedule Solver.
Hanya berisi Dataclass dan class penyimpan state (VariableStore).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from ortools.sat.python import cp_model


@dataclass
class Person:
    """Representasi personel yang akan dijadwalkan."""
    name: str
    is_ecom: bool = False


@dataclass
class DaySchedule:
    """Representasi hari dalam jadwal."""
    day_index: int
    date_str: str


@dataclass
class Assignment:
    """Data sel dari template Excel."""
    person_name: str
    day_index: int
    label: str  # Bisa '1', 'A', 'B', 'C', atau kosong
    is_locked: bool


@dataclass
class WorkbookData:
    """Struktur data representasi dari seluruh isi Excel."""
    people: List[Person]
    schedules: List[DaySchedule]
    assignments: List[Assignment]
    row_lookup: Dict[str, int] = field(default_factory=dict)
    day_lookup: Dict[int, int] = field(default_factory=dict)


class VariableStore:
    """Penyimpanan dan antarmuka untuk variabel CP-SAT (menggunakan IntVar)."""
    
    def __init__(self, model: cp_model.CpModel):
        self.model = model
        # Struktur: _vars[person_name][day_index][label] = IntVar
        self._vars: Dict[str, Dict[int, Dict[str, cp_model.IntVar]]] = {}

    def create(self, person: str, day: int, label: str) -> cp_model.IntVar:
        """Membuat variabel boolean baru untuk solver."""
        if person not in self._vars:
            self._vars[person] = {}
        if day not in self._vars[person]:
            self._vars[person][day] = {}
            
        var_name = f"assign_{person}_day{day}_{label}"
        # NewBoolVar tetap digunakan untuk membuat variabelnya
        var = self.model.NewBoolVar(var_name)
        self._vars[person][day][label] = var
        return var

    def get(self, person: str, day: int, label: str) -> Optional[cp_model.IntVar]:
        """Mengambil variabel boolean secara spesifik."""
        return self._vars.get(person, {}).get(day, {}).get(label)

    def labels(self, person: str, day: int) -> List[cp_model.IntVar]:
        """Mengambil seluruh variabel label (A, B, C) untuk satu orang di satu hari."""
        day_vars = self._vars.get(person, {}).get(day, {})
        return list(day_vars.values())

    def day_label(self, day: int, label: str) -> List[cp_model.IntVar]:
        """Mengambil seluruh variabel dari personel berbeda untuk hari dan label tertentu."""
        result = []
        for person, days in self._vars.items():
            if day in days and label in days[day]:
                result.append(days[day][label])
        return result

    def person_history(self, person: str, label: str) -> List[cp_model.IntVar]:
        """Mengambil riwayat variabel dari hari ke hari untuk satu orang dan satu label."""
        result = []
        person_days = self._vars.get(person, {})
        # Sort berdasarkan day_index agar urut secara kronologis
        for day in sorted(person_days.keys()):
            if label in person_days[day]:
                result.append(person_days[day][label])
        return result


# --- Model Hasil & Validasi ---

@dataclass
class SolverResult:
    """Hasil akhir dari eksekusi CP-SAT."""
    status: int
    assignments: Dict[str, Dict[int, str]]
    objective_value: float
    solve_time_seconds: float


@dataclass
class ValidationIssue:
    """Temuan isu saat memvalidasi jadwal."""
    rule_name: str
    person: str
    day_index: int
    description: str


@dataclass
class ValidationResult:
    """Kumpulan hasil validasi jadwal."""
    is_valid: bool
    issues: List[ValidationIssue]


@dataclass
class PersonStatistic:
    """Statistik jumlah shift per personel."""
    person_name: str
    count_a: int = 0
    count_b: int = 0
    count_c: int = 0
    total_shifts: int = 0


@dataclass
class ReportData:
    """Data yang dikumpulkan untuk generate laporan akhir."""
    solver_status: str
    validation: ValidationResult
    statistics: List[PersonStatistic]
    
