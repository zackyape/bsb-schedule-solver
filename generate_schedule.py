"""
generate_schedule.py
Entry point for BSB Schedule Solver v2
"""

from excel_io import ExcelIO
from optimizer import ScheduleOptimizer
from validator import ScheduleValidator
from report import ReportGenerator


def main():
    print("=" * 60)
    print("BSB Schedule Solver v2")
    print("=" * 60)

    excel = ExcelIO()
    workbook = excel.load()

    optimizer = ScheduleOptimizer(workbook)
    result = optimizer.solve()

    if not result.solved:
        print("No feasible solution found.")
        return

    validator = ScheduleValidator()
    validation = validator.validate(workbook, result)

    if validation.passed:
        print("[OK] Validation passed.")
    else:
        print(f"[WARNING] Validation failed ({len(validation.issues)} issue(s)).")
        for issue in validation.issues:
            person = issue.person or "-"
            day = issue.day if issue.day is not None else "-"
            print(f"  - {issue.rule}: person={person}, day={day}, {issue.message}")

    excel.save(result)

    report = ReportGenerator(
        workbook=workbook,
        result=result,
        validation=validation,
    )
    report.generate()

    print("Done.")
    print("Excel exported.")
    print("Reports generated.")


if __name__ == "__main__":
    main()
    
