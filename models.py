"""
models.py

Data models for BSB Schedule Solver v2
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(slots=True)
class Assignment:
    day: int
    label: Optional[str]
    locked: bool = False


@dataclass(slots=True)
class Person:
    name: str
    row: int
    assignments: List[Assignment] = field(default_factory=list)


@dataclass(slots=True)
class DaySchedule:
    day: int
    personnel: List[str] = field(default_factory=list)
    locked: Dict[str, str] = field(default_factory=dict)
    empty: List[str] = field(default_factory=list)


@dataclass(slots=True)
class WorkbookData:
    people: Dict[str, Person]
    days: List[DaySchedule]


@dataclass(slots=True)
class SolverResult:
    solved: bool
    objective_value: float
    assignments: Dict[int, Dict[str, str]]
    row_lookup: Dict[str, int]


@dataclass(slots=True)
class ValidationIssue:
    rule: str
    person: Optional[str]
    day: Optional[int]
    message: str


@dataclass(slots=True)
class ValidationResult:
    passed: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    
