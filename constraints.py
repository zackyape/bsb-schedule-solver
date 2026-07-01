"""
constraints.py
Constraint builder for BSB Schedule Solver
"""

from ortools.sat.python import cp_model


class ConstraintBuilder:

    def __init__(self, model, variables):
        self.model = model
        self.x = variables

    # -------------------------------------------------------
    # Every day must contain exactly:
    # A
    # B
    # C
    # -------------------------------------------------------

    def daily_abc(self, active_people):

        for day, people in active_people.items():

            for label in ("A", "B", "C"):

                self.model.Add(
                    sum(
                        self.x[(person, day, label)]
                        for person in people
                    ) == 1
                )

            for person in people:

                self.model.Add(
                    sum(
                        self.x[(person, day, l)]
                        for l in ("A", "B", "C")
                    ) == 1
                )

    # -------------------------------------------------------

    def locked_cells(self, locked):

        for person, day, label in locked:

            self.model.Add(
                self.x[(person, day, label)] == 1
            )

    # -------------------------------------------------------

    def no_repeat(self, history):

        for person, days in history.items():

            for i in range(len(days) - 1):

                d1 = days[i]
                d2 = days[i + 1]

                for label in ("A", "B", "C"):

                    self.model.Add(

                        self.x[(person, d1, label)]

                        +

                        self.x[(person, d2, label)]

                        <= 1

                    )

    # -------------------------------------------------------

    def no_abab(self, history):

        bad_patterns = [

            ("A", "B"),
            ("B", "A"),

            ("A", "C"),
            ("C", "A"),

            ("B", "C"),
            ("C", "B"),

        ]

        for person, days in history.items():

            for i in range(len(days) - 3):

                d1 = days[i]
                d2 = days[i + 1]
                d3 = days[i + 2]
                d4 = days[i + 3]

                for a, b in bad_patterns:

                    self.model.Add(

                        self.x[(person, d1, a)]

                        +

                        self.x[(person, d2, b)]

                        +

                        self.x[(person, d3, a)]

                        +

                        self.x[(person, d4, b)]

                        <= 3

                    )

    # -------------------------------------------------------
    # Soft constraint
    # max 1 C each week
    # -------------------------------------------------------

    def weekly_c_limit(self,
                       history,
                       week_map):

        penalties = []

        for person, days in history.items():

            for week, week_days in week_map.items():

                vars_ = []

                for day in days:

                    if day in week_days:

                        vars_.append(

                            self.x[(person, day, "C")]

                        )

                if vars_:

                    extra = self.model.NewIntVar(
                        0,
                        10,
                        f"extra_{person}_{week}"
                    )

                    self.model.Add(

                        extra

                        >=

                        sum(vars_) - 1

                    )

                    penalties.append(extra)

        return penalties

    # -------------------------------------------------------

    def balance(self,
                history):

        penalties = []

        for person, days in history.items():

            total = len(days)

            target = total // 3

            for label in ("A", "B", "C"):

                count = self.model.NewIntVar(
                    0,
                    total,
                    f"{person}_{label}"
                )

                self.model.Add(

                    count

                    ==

                    sum(

                        self.x[(person, d, label)]

                        for d in days

                    )

                )

                diff = self.model.NewIntVar(
                    0,
                    total,
                    f"diff_{person}_{label}"
                )

                self.model.AddAbsEquality(
                    diff,
                    count - target
                )

                penalties.append(diff)

        return penalties
