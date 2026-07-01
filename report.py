"""
report.py
"""

from collections import defaultdict

from config import REPORT_FILE, LABELS, WEEKS


class ReportGenerator:

    def __init__(self, history, result):

        self.history = history
        self.result = result

    def build(self):

        label_count = defaultdict(lambda: defaultdict(int))
        week_c = defaultdict(lambda: defaultdict(int))

        for day, assign in self.result.items():

            week = self._week(day)

            for person, label in assign.items():

                label_count[person][label] += 1

                if label == "C":
                    week_c[person][week] += 1

        with open(REPORT_FILE, "w", encoding="utf-8") as f:

            f.write("=" * 60 + "\n")
            f.write("BSB SCHEDULE REPORT\n")
            f.write("=" * 60 + "\n\n")

            for person in sorted(label_count.keys()):

                f.write(f"{person}\n")
                f.write("-" * 40 + "\n")

                total = 0

                for label in LABELS:

                    value = label_count[person][label]

                    total += value

                    f.write(f"{label} : {value}\n")

                f.write(f"TOTAL : {total}\n\n")

                f.write("Weekly C\n")

                for week in sorted(WEEKS.keys()):

                    c = week_c[person][week]

                    if c <= 1:
                        status = "OK"
                    else:
                        status = "WARNING"

                    f.write(
                        f"Week {week} : {c} ({status})\n"
                    )

                f.write("\n")

    def _week(self, day):

        for week, days in WEEKS.items():

            if day in days:
                return week

        return 0
