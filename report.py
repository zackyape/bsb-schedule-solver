"""
report.py
Generate TXT and CSV reports.
"""
from collections import defaultdict
import csv
from config import REPORT_TXT, REPORT_CSV, LABELS, calendar

class ReportGenerator:
    def __init__(self, workbook, result, validation):
        self.workbook=workbook
        self.result=result
        self.validation=validation

    def generate(self):
        stats=defaultdict(lambda: defaultdict(int))
        weekly=defaultdict(lambda: defaultdict(int))

        for day,assign in self.result.assignments.items():
            week=next((w for w,r in calendar.weeks.items() if day in r),0)
            for person,label in assign.items():
                stats[person][label]+=1
                if label=="C":
                    weekly[person][week]+=1

        with open(REPORT_TXT,"w",encoding="utf-8") as f:
            f.write("BSB SCHEDULE REPORT\n\n")
            f.write(f"Validation: {'PASS' if self.validation.passed else 'FAIL'}\n\n")
            for p in sorted(stats):
                f.write(f"{p}\n")
                for l in LABELS:
                    f.write(f"  {l}: {stats[p][l]}\n")
                for w in sorted(calendar.weeks):
                    f.write(f"  Week {w} C: {weekly[p][w]}\n")
                f.write("\n")
            if self.validation.issues:
                f.write("Issues:\n")
                for i in self.validation.issues:
                    f.write(f"- {i.rule}: {i.message}\n")

        with open(REPORT_CSV,"w",newline="",encoding="utf-8") as f:
            writer=csv.writer(f)
            writer.writerow(["Person","A","B","C"])
            for p in sorted(stats):
                writer.writerow([p,stats[p]["A"],stats[p]["B"],stats[p]["C"]])
              
