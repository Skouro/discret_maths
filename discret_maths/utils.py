# Standar imports
from typing import Set


def calculate_dividers(number: int) -> Set[int]:
    result = set()
    for divisor in range(1, number + 1):
        if (number % divisor) == 0:
            result.add(divisor)
    return set(sorted(result))
