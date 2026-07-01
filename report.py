"""
Report Module untuk BSB Schedule Solver V2.1.
Mengolah hasil solver dan validasi menjadi output laporan.
"""

from models import SolverResult, ValidationResult, ReportData, PersonStatistic, WorkbookData
import pandas as pd

class ReportGenerator:
    """Mengenerate file txt, csv, dan excel summary."""

    @staticmethod
    def generate(result: SolverResult, validation: ValidationResult, data: WorkbookData) -> ReportData:
        # Hitung statistik
        stats = []
        for person in data.people:
            p_assignments = result.assignments.get(person.name, {})
            stats.append(PersonStatistic(
                person_name=person.name,
                count_a=list(p_assignments.values()).count("A"),
                count_b=list(p_assignments.values()).count("B"),
                count_c=list(p_assignments.values()).count("C"),
                total_shifts=len(p_assignments)
            ))
        
        # Simpan ke file excel
        df = pd.DataFrame([vars(s) for s in stats])
        df.to_excel("statistics.xlsx", index=False)
        
        # Simpan summary ke txt
        with open("report.txt", "w") as f:
            f.write(f"Solver Status: {result.status}\n")
            f.write(f"Objective Value: {result.objective_value}\n")
            f.write(f"Validation: {'PASSED' if validation.is_valid else 'FAILED'}\n")
            
        return ReportData(str(result.status), validation, stats)
        
