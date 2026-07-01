"""
validator.py
Validation layer for BSB Schedule Solver v2
"""
from collections import defaultdict
from models import ValidationIssue, ValidationResult
from config import calendar

class ScheduleValidator:
    def validate(self, workbook, result):
        issues=[]

        # Daily ABC
        for day,assign in result.assignments.items():
            labels=sorted(assign.values())
            if labels!=["A","B","C"]:
                issues.append(
                    ValidationIssue(
                        rule="DailyABC",
                        person=None,
                        day=day,
                        message="Daily labels are not exactly A,B,C",
                    )
                )

        # Locked cells
        for ds in workbook.days:
            solved=result.assignments.get(ds.day,{})
            for person,label in ds.locked.items():
                if solved.get(person)!=label:
                    issues.append(
                        ValidationIssue(
                            rule="Locked",
                            person=person,
                            day=ds.day,
                            message="Locked value changed",
                        )
                    )

        # Per person history
        history=defaultdict(list)
        for day in sorted(result.assignments):
            for person,label in result.assignments[day].items():
                history[person].append((day,label))

        bad={("A","B","A","B"),("B","A","B","A"),
             ("A","C","A","C"),("C","A","C","A"),
             ("B","C","B","C"),("C","B","C","B")}

        for person,seq in history.items():
            # no repeat
            for i in range(len(seq)-1):
                if seq[i][1]==seq[i+1][1]:
                    issues.append(
                        ValidationIssue(
                            rule="NoRepeat",
                            person=person,
                            day=seq[i+1][0],
                            message="Repeated label",
                        )
                    )
            # no ABAB
            for i in range(len(seq)-3):
                p=(seq[i][1],seq[i+1][1],seq[i+2][1],seq[i+3][1])
                if p in bad:
                    issues.append(
                        ValidationIssue(
                            rule="NoABAB",
                            person=person,
                            day=seq[i+3][0],
                            message=f"Forbidden pattern {p}",
                        )
                    )
            # weekly C
            for week,days in calendar.weeks.items():
                c=sum(1 for d,l in seq if d in days and l=="C")
                if c>1:
                    issues.append(
                        ValidationIssue(
                            rule="WeeklyC",
                            person=person,
                            day=None,
                            message=f"Week {week}: C={c}",
                        )
                    )

        return ValidationResult(
            passed=len(issues)==0,
            issues=issues,
        )
      
