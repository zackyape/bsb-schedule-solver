"""
Validator Module untuk BSB Schedule Solver V2.1.
Mengecek integritas hasil solver terhadap aturan bisnis sebelum laporan dibuat.
"""

from models import SolverResult, WorkbookData, ValidationResult, ValidationIssue
from config import LABELS

class ScheduleValidator:
    """Kelas untuk melakukan validasi pasca-optimasi."""

    def __init__(self, data: WorkbookData):
        self.data = data

    def validate(self, result: SolverResult) -> ValidationResult:
        """Menjalankan seluruh pengecekan rule pada hasil assignment."""
        issues = []
        
        # 1. Cek Locked Cells (Harus tetap sesuai template awal)
        for assignment in self.data.assignments:
            if assignment.is_locked:
                assigned = result.assignments.get(assignment.person_name, {}).get(assignment.day_index)
                if assigned != assignment.label:
                    issues.append(ValidationIssue(
                        "LockedRule", assignment.person_name, assignment.day_index,
                        f"Sel terkunci berubah dari {assignment.label} menjadi {assigned}"
                    ))

        # 2. Cek AA, BB, CC (No Repeat)
        for person in self.data.people:
            for day_idx in range(len(self.data.schedules) - 1):
                label_today = result.assignments.get(person.name, {}).get(day_idx)
                label_tomorrow = result.assignments.get(person.name, {}).get(day_idx + 1)
                
                if label_today and label_today == label_tomorrow:
                    issues.append(ValidationIssue(
                        "NoRepeatRule", person.name, day_idx,
                        f"Terdeteksi repetisi {label_today}{label_tomorrow}"
                    ))

        # 3. Cek ABAB, ACAC, BCBC (No Patterns)
        # Sederhanakan pengecekan pola 4 hari
        for person in self.data.people:
            for i in range(len(self.data.schedules) - 3):
                p = [result.assignments.get(person.name, {}).get(d) for d in range(i, i+4)]
                if None not in p:
                    if p[0] == p[2] and p[1] == p[3] and p[0] != p[1]:
                        issues.append(ValidationIssue(
                            "NoPatternRule", person.name, i,
                            f"Pola repetitif terlarang terdeteksi: {''.join(p)}"
                        ))

        # 4. Cek Kelengkapan Harian (Harus ada A, B, C)
        for day in self.data.schedules:
            daily_labels = [result.assignments.get(p.name, {}).get(day.day_index) for p in self.data.people]
            for lbl in LABELS:
                if daily_labels.count(lbl) != 1:
                    issues.append(ValidationIssue(
                        "DailyABCRule", "ALL", day.day_index,
                        f"Label {lbl} muncul {daily_labels.count(lbl)} kali pada hari {day.day_index}"
                    ))

        return ValidationResult(is_valid=len(issues) == 0, issues=issues)
        
