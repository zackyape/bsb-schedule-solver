"""
utils.py

Common helper functions for BSB Schedule Solver.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Sequence

from models import Assignment


# ============================================================
# Assignment Helpers
# ============================================================

def sort_assignments(
    assignments: list[Assignment],
) -> list[Assignment]:
    """
    Return assignments sorted by day.
    """
    return sorted(assignments, key=lambda item: item.day)


# ============================================================
# History Helpers
# ============================================================

def assignment_labels(
    assignments: list[Assignment],
) -> list[str]:
    """
    Return assignment labels.

    Example:
        [A, C, B]
    """
    labels = []

    for assignment in sort_assignments(assignments):

        if assignment.label is None:
            continue

        labels.append(
            assignment.label
        )

    return labels


def assignment_days(
    assignments: list[Assignment],
) -> list[int]:
    """
    Return assignment days.
    """

    return [
        assignment.day
        for assignment in sort_assignments(assignments)
    ]


# ============================================================
# Pattern Helpers
# ============================================================

def has_consecutive_repeat(
    labels: Sequence[str],
) -> bool:
    """
    Detect:

    AA
    BB
    CC
    """

    for current, nxt in zip(labels, labels[1:]):

        if current == nxt:
            return True

    return False


def has_abab_pattern(
    labels: Sequence[str],
) -> bool:
    """
    Detect:

    ABAB
    ACAC
    BCBC

    and reverse.
    """

    if len(labels) < 4:
        return False

    for i in range(len(labels) - 3):

        a = labels[i]
        b = labels[i + 1]
        c = labels[i + 2]
        d = labels[i + 3]

        if (
            a == c
            and b == d
            and a != b
        ):
            return True

    return False


# ============================================================
# Weekly Helpers
# ============================================================

def weekly_counter(
    assignments: list[Assignment],
    weeks: dict[int, range],
) -> dict[int, int]:
    """
    Count C assignment for every week.
    """

    result = defaultdict(int)

    for assignment in assignments:

        if assignment.label != "C":
            continue

        for week, days in weeks.items():

            if assignment.day in days:

                result[week] += 1

                break

    return dict(result)


# ============================================================
# Statistics
# ============================================================

def label_counter(
    assignments: list[Assignment],
) -> dict[str, int]:
    """
    Count A/B/C.
    """

    counter = {
        "A": 0,
        "B": 0,
        "C": 0,
    }

    for assignment in assignments:

        if assignment.label is None:
            continue

        counter[assignment.label] += 1

    return counter


# ============================================================
# Generic Helpers
# ============================================================

def flatten(
    values: Iterable[Iterable],
):
    """
    Flatten nested iterable.
    """

    for value in values:

        yield from value


def pairwise(
    values: Sequence,
):
    """
    Iterate pairwise.

    Example:

    A B C D

    →

    AB
    BC
    CD
    """

    for i in range(len(values) - 1):

        yield values[i], values[i + 1]


# ============================================================
# Debug
# ============================================================

def print_title(
    title: str,
):
    """
    Pretty title.
    """

    line = "=" * 60

    print()

    print(line)

    print(title)

    print(line)
