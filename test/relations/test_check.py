# pylint:disable=unused-argument
# type: ignore

from test.relations import build_graph
import pytest
from networkx.classes.digraph import DiGraph
from discret_maths.relations import check


@pytest.mark.parametrize(
    "domain,relations,check_func,result",
    [
        (
            {2, 4, 5, 6, 7},
            {(2, 2), (4, 4), (5, 5), (6, 6), (7, 7)},
            check.is_reflexive,
            True,
        ),
        (
            {2, 4, 5, 6, 7},
            {(2, 2), (4, 2), (5, 5), (6, 6), (7, 6)},
            check.is_reflexive,
            False,
        ),
        (
            {2, 4, 5, 6, 7},
            {(4, 5), (2, 4), (5, 2), (6, 7), (7, 6)},
            check.is_anti_reflexive,
            True,
        ),
        (
            {2, 4, 5, 6, 7},
            {(4, 5), (2, 2), (5, 2), (6, 6), (7, 6)},
            check.is_anti_reflexive,
            False,
        ),
        (
            {2, 4, 5, 6, 7},
            {(2, 2), (4, 4), (5, 6), (6, 5), (7, 7)},
            check.is_not_reflexive,
            True,
        ),
        (
            {2, 4, 5, 6, 7},
            {(4, 4), (2, 2), (5, 5), (6, 6), (7, 7)},
            check.is_not_reflexive,
            False,
        ),
        (
            {2, 4, 5, 6, 7},
            {(2, 2), (6, 4), (5, 6), (6, 5), (4, 6)},
            check.is_symmetric,
            True,
        ),
        (
            {2, 4, 5, 6, 7},
            {(2, 2), (2, 6), (6, 4), (5, 6), (5, 4), (6, 5), (4, 6)},
            check.is_symmetric,
            False,
        ),
        (
            {2, 4, 5, 6, 7},
            {(2, 2), (6, 4), (5, 6), (6, 2), (4, 5), (7, 7)},
            check.is_anti_symmetric,
            True,
        ),
        (
            {2, 4, 5, 6, 7},
            {(2, 2), (6, 4), (5, 6), (6, 2), (2, 6), (4, 5), (7, 7)},
            check.is_anti_symmetric,
            False,
        ),
    ],
)
@build_graph()
def test_relations(
    graph: DiGraph,
    domain,
    relations,
    check_func,
    result,
) -> None:
    assert check_func(graph) is result
