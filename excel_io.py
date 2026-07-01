"""
excel_io.py

Excel reader/writer for BSB Schedule Solver.
"""

from dataclasses import dataclass
from typing import Dict, List

from openpyxl import load_workbook

from config import (
    INPUT_FILE,
    OUTPUT_FILE,
    SHEET_NAME,
    PERSONNEL,
    ROW_MAP,
    FIRST_DAY_COLUMN,
    LAST_DAY_COLUMN,
)

LOCKED = {"A", "B", "C"}


@dataclass
class DayAssignment:
    day: int
    active: List[str]
    locked: Dict[str, str]
    empty: List[str]


class ExcelIO:

    def __init__(self):
        self.wb = load_workbook(INPUT_FILE)
        self.ws = self.wb[SHEET_NAME]

    def load_schedule(self) -> List[DayAssignment]:
        days = []

        for col in range(FIRST_DAY_COLUMN, LAST_DAY_COLUMN + 1):

            day = col - 1

            active = []
            locked = {}
            empty = []

            for person in PERSONNEL:

                row = ROW_MAP[person]
                value = self.ws.cell(row=row, column=col).value

                if value is None:
                    continue

                if value in LOCKED:
                    active.append(person)
                    locked[person] = value

                elif value == 1:
                    active.append(person)
                    empty.append(person)

            days.append(
                DayAssignment(
                    day=day,
                    active=active,
                    locked=locked,
                    empty=empty,
                )
            )

        return days

    def write_result(self, result: Dict[int, Dict[str, str]]):

        for day, assignment in result.items():

            col = day + 1

            for person, label in assignment.items():

                row = ROW_MAP[person]

                self.ws.cell(row=row, column=col).value = label

        self.wb.save(OUTPUT_FILE)
