# type: ignore
from test.relations import build_graph
import pytest
from networkx.classes.digraph import DiGraph
from discret_maths.relations import extract


@pytest.mark.parametrize(
    "node_x,node_y,result",
    [
        (1, 2, {2, 4, 10, 20}),
        (1, 4, {4, 20}),
        (1, 5, {5, 10, 20}),
        (2, 5, {10, 20}),
        (2, 20, {20}),
        (5, 20, {20}),
        (5, 10, {10, 20}),
    ],
)
@build_graph(
    domain={1, 2, 4, 5, 10, 20},
    relations={(1, 2), (1, 5), (2, 4), (5, 10), (2, 10), (4, 20), (10, 20)},
)
def test_get_cs(graph: DiGraph, node_x, node_y, result) -> None:
    assert extract.get_cs(graph, node_x, node_y) == result


@pytest.mark.parametrize(
    "node_x,node_y,result",
    [
        (2, 4, {1, 2}),
        (1, 2, {1}),
        (1, 20, {1}),
        (1, 5, {1}),
        (2, 4, {1, 2}),
    ],
)
@build_graph(
    domain={1, 2, 4, 5, 10, 20},
    relations={(1, 2), (1, 5), (2, 4), (2, 10), (4, 20), (10, 20)},
)
def test_get_ci(graph: DiGraph, node_x, node_y, result) -> None:
    assert extract.get_ci(graph, node_x, node_y) == result
