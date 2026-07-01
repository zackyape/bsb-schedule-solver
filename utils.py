"""
utils.py

Utility functions for BSB Schedule Solver V2.1
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import pairwise
from typing import Iterable

from models import Assignment


# ==========================================================
# SORTING
# ==========================================================

def sort_assignments(
    assignments: list[Assignment],
) -> list[Assignment]:
    """
    Return assignments sorted by day.
    """

    return sorted(
        assignments,
        key=lambda x: x.day,
    )


# ==========================================================
# LABELS
# ==========================================================

def assignment_labels(
    assignments: list[Assignment],
) -> list[str]:
    """
    Extract labels only.

    Example:
        A B C A
    """

    labels = []

    for assignment in sort_assignments(assignments):

        if assignment.label is None:
            continue

        labels.append(
            assignment.label
        )

    return labels


# ==========================================================
# DAYS
# ==========================================================

def assignment_days(
    assignments: list[Assignment],
) -> list[int]:

    return [

        assignment.day

        for assignment

        in sort_assignments(assignments)

    ]


# ==========================================================
# COUNTER
# ==========================================================

def count_labels(
    assignments: list[Assignment],
) -> Counter:

    return Counter(
        assignment_labels(assignments)
    )


# ==========================================================
# WEEKLY C
# ==========================================================

def weekly_counter(
    assignments: list[Assignment],
    weeks: dict[int, range],
) -> dict[int, int]:

    result = defaultdict(int)

    for assignment in assignments:

        if assignment.label != "C":
            continue

        for week, days in weeks.items():

            if assignment.day in days:

                result[week] += 1

                break

    return dict(result)


# ==========================================================
# PATTERN
# ==========================================================

def has_repeat(
    labels: list[str],
) -> bool:
    """
    AA
    BB
    CC
    """

    for a, b in pairwise(labels):

        if a == b:
            return True

    return False


def has_abab(
    labels: list[str],
) -> bool:
    """
    ABAB
    ACAC
    BCBC
    """

    if len(labels) < 4:
        return False

    for i in range(len(labels) - 3):

        a = labels[i]
        b = labels[i + 1]
        c = labels[i + 2]
        d = labels[i + 3]

        if a == c and b == d and a != b:

            return True

    return False


# ==========================================================
# BALANCE
# ==========================================================

def balance_score(
    assignments: list[Assignment],
) -> int:
    """
    Lower is better.
    """

    counter = count_labels(assignments)

    if not counter:
        return 0

    values = [

        counter.get("A", 0),

        counter.get("B", 0),

        counter.get("C", 0),

    ]

    return max(values) - min(values)


# ==========================================================
# GROUP
# ==========================================================

def group_by_week(
    assignments: list[Assignment],
    weeks: dict[int, range],
):

    grouped = defaultdict(list)

    for assignment in assignments:

        for week, days in weeks.items():

            if assignment.day in days:

                grouped[week].append(
                    assignment
                )

                break

    return grouped


# ==========================================================
# FLATTEN
# ==========================================================

def flatten(
    values: Iterable[Iterable],
):

    for value in values:

        yield from value


# ==========================================================
# WINDOW
# ==========================================================

def sliding_window(
    items: list,
    size: int,
):

    if size <= 0:
        return

    for i in range(len(items) - size + 1):

        yield items[i:i + size]


# ==========================================================
# PRETTY PRINT
# ==========================================================

def print_title(
    title: str,
):

    print()

    print("=" * 60)

    print(title)

    print("=" * 60)
