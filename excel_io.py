"""
excel_io.py

Read / Write Excel workbook.

BSB Schedule Solver v2
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from openpyxl import load_workbook

from config import (
    INPUT_FILE,
    OUTPUT_FILE,
    excel,
    LOCK_VALUES,
    EMPTY_VALUES,
    IGNORE_PERSONNEL,
)

from models import (
    Assignment,
    DaySchedule,
    Person,
    WorkbookData,
)


class ExcelIO:

    def __init__(
        self,
        input_file: Path = INPUT_FILE,
    ):

        self.input_file = Path(input_file)

        self.workbook = load_workbook(self.input_file)

        if excel.auto_detect_sheet:
            self.sheet = self.workbook.active
        else:
            self.sheet = self.workbook[
                excel.sheet_name
            ]

    # ------------------------------------------------------

    def load(self) -> WorkbookData:

        people = self._load_people()

        days = self._load_days(
            people
        )

        return WorkbookData(
            people=people,
            days=days,
        )

    # ------------------------------------------------------

    def save(
        self,
        result,
        output_file: Path = OUTPUT_FILE,
    ):

        for day, values in result.assignments.items():

            column = self._day_to_column(day)

            for person_name, label in values.items():

                row = result.row_lookup[
                    person_name
                ]

                self.sheet.cell(
                    row=row,
                    column=column,
                ).value = label

        self.workbook.save(output_file)

    # ------------------------------------------------------

    def _load_people(
        self,
    ) -> Dict[str, Person]:

        people = {}

        row = self._find_header_row()

        row += 1

        while True:

            name = self.sheet.cell(
                row=row,
                column=1,
            ).value

            if not name:
                break

            name = str(name).strip()

            if name in IGNORE_PERSONNEL:

                row += 1

                continue

            people[name] = Person(
                name=name,
                row=row,
            )

            row += 1

        return people

    # ------------------------------------------------------

    def _load_days(
        self,
        people,
    ):

        schedules = []

        for column in range(
            excel.first_day_column,
            excel.last_day_column + 1,
        ):

            day = self.sheet.cell(
                row=4,
                column=column,
            ).value

            if not isinstance(day, int):
                continue

            schedule = DaySchedule(
                day=day,
            )

            for person in people.values():

                value = self.sheet.cell(
                    row=person.row,
                    column=column,
                ).value

                if value is None:
                    continue

                if value in LOCK_VALUES:

                    schedule.personnel.append(
                        person.name
                    )

                    schedule.locked[
                        person.name
                    ] = value

                    person.assignments.append(
                        Assignment(
                            day=day,
                            label=value,
                            locked=True,
                        )
                    )

                elif value in EMPTY_VALUES:

                    schedule.personnel.append(
                        person.name
                    )

                    schedule.empty.append(
                        person.name
                    )

                    person.assignments.append(
                        Assignment(
                            day=day,
                            label=None,
                            locked=False,
                        )
                    )

            schedules.append(
                schedule
            )

        return schedules

    # ------------------------------------------------------

    def _find_header_row(self):

        for row in range(
            1,
            self.sheet.max_row + 1,
        ):

            value = self.sheet.cell(
                row=row,
                column=1,
            ).value

            if value is None:
                continue

            if (
                str(value)
                .strip()
                .upper()
                == "NAMA / TANGGAL"
            ):
                return row

        raise RuntimeError(
            "Header 'NAMA / TANGGAL' tidak ditemukan."
        )

    # ------------------------------------------------------

    @staticmethod
    def _day_to_column(
        day: int,
    ) -> int:

        return excel.first_day_column + day - 1
