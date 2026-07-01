"""
constraints.py
Hard constraint plugins
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict
from ortools.sat.python import cp_model
from models import WorkbookData

class Constraint(ABC):
    name="Constraint"
    @abstractmethod
    def apply(self, model:cp_model.CpModel, variables:dict, workbook:WorkbookData)->None: ...

class DailyABCConstraint(Constraint):
    name="DailyABC"
    def apply(self, model, variables, workbook):
        for day in workbook.days:
            for label in ("A","B","C"):
                model.Add(sum(variables[(p,day.day,label)] for p in day.personnel)==1)
            for p in day.personnel:
                model.Add(sum(variables[(p,day.day,l)] for l in ("A","B","C"))==1)

class LockedConstraint(Constraint):
    name="Locked"
    def apply(self, model, variables, workbook):
        for day in workbook.days:
            for p,l in day.locked.items():
                model.Add(variables[(p,day.day,l)]==1)

class NoRepeatConstraint(Constraint):
    name="NoRepeat"
    def apply(self, model, variables, workbook):
        for person in workbook.people.values():
            a=sorted(person.assignments,key=lambda x:x.day)
            for i in range(len(a)-1):
                for l in ("A","B","C"):
                    model.Add(
                        variables[(person.name,a[i].day,l)] +
                        variables[(person.name,a[i+1].day,l)] <= 1
                    )

class NoABABConstraint(Constraint):
    BAD=[("A","B"),("B","A"),("A","C"),("C","A"),("B","C"),("C","B")]
    name="NoABAB"
    def apply(self, model, variables, workbook):
        for person in workbook.people.values():
            a=sorted(person.assignments,key=lambda x:x.day)
            for i in range(len(a)-3):
                d=[x.day for x in a[i:i+4]]
                for x,y in self.BAD:
                    model.Add(
                        variables[(person.name,d[0],x)] +
                        variables[(person.name,d[1],y)] +
                        variables[(person.name,d[2],x)] +
                        variables[(person.name,d[3],y)] <= 3
                    )

DEFAULT_CONSTRAINTS=[
    DailyABCConstraint(),
    LockedConstraint(),
    NoRepeatConstraint(),
    NoABABConstraint(),
]

