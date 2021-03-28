# Standar imports
from typing import (
    Any,
    Optional,
    Set,
    Tuple,
)


def calculate_dividers(number: int) -> Set[int]:
    result = set()
    for divisor in range(1, number + 1):
        if (number % divisor) == 0:
            result.add(divisor)
    return set(sorted(result))


def get_set_combination(
    domain: Set[Any],
    image: Optional[Set[Any]] = None,
) -> Set[Tuple[Any, Any]]:
    image = image or domain
    return set((node_x, node_y) for node_x in domain for node_y in image)
