"""
generate_schedule.py
"""

from excel_io import ExcelIO
from optimizer import ScheduleOptimizer
from report import ReportGenerator
from config import WEEKS


def build_history(days):

    history = {}

    locked = []

    for day in days:

        for person in day.active:

            history.setdefault(person, []).append(day.day)

        for person, label in day.locked.items():

            locked.append(
                (
                    person,
                    day.day,
                    label,
                )
            )

    return history, locked


def main():

    excel = ExcelIO()

    days = excel.load_schedule()

    history, locked = build_history(days)

    solver = ScheduleOptimizer(
        days=days,
        history=history,
        locked=locked,
        weeks=WEEKS,
    )

    result = solver.solve()

    if result is None:

        print("Tidak ditemukan solusi.")

        return

    excel.write_result(result)

    report = ReportGenerator(
        history,
        result,
    )

    report.build()

    print("=================================")
    print("Schedule berhasil dibuat")
    print("=================================")


if __name__ == "__main__":
    main()
