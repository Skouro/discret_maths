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
        (5, 20, {1, 5}),
        (5, 10, {1, 5}),
    ],
)
@build_graph(
    domain={1, 2, 4, 5, 10, 20},
    relations={(1, 2), (1, 5), (2, 4), (5, 10), (2, 10), (4, 20), (10, 20)},
)
def test_get_ci(graph: DiGraph, node_x, node_y, result) -> None:
    assert extract.get_ci(graph, node_x, node_y) == result


@pytest.mark.parametrize(
    "node_x,node_y,result",
    [
        (1, 2, 2),
        (1, 4, 4),
        (4, 10, 20),
        (2, 20, 20),
        (5, 10, 10),
    ],
)
@build_graph(
    domain={1, 2, 4, 5, 10, 20},
    relations={(1, 2), (1, 5), (2, 4), (5, 10), (2, 10), (4, 20), (10, 20)},
)
def test_get_mcs(graph: DiGraph, node_x, node_y, result) -> None:
    assert extract.get_mcs(graph, node_x, node_y) == result


@pytest.mark.parametrize(
    "node_x,node_y,result",
    [
        (1, 2, 1),
        (1, 4, 1),
        (1, 10, 1),
        (2, 4, 2),
        (5, 20, 5),
    ],
)
@build_graph(
    domain={1, 2, 4, 5, 10, 20},
    relations={(1, 2), (1, 5), (2, 4), (5, 10), (2, 10), (4, 20), (10, 20)},
)
def test_get_mci(graph: DiGraph, node_x, node_y, result) -> None:
    assert extract.get_mci(graph, node_x, node_y) == result


@pytest.mark.parametrize(
    "node_x,node_y,result",
    [
        ('a', 'b', None),
        ('d', 'e', 'c'),
        ('f', 'g', None),
    ],
)
@build_graph(
    domain={'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'},
    relations=(
        ('a', 'c'),
        ('b', 'c'),
        ('c', 'e'),
        ('c', 'd'),
        ('d', 'f'),
        ('d', 'g'),
        ('e', 'f'),
        ('e', 'g'),
        ('f', 'h'),
        ('g', 'h'),
    ),
)
def test_get_mci_fail(graph: DiGraph, node_x, node_y, result) -> None:
    assert extract.get_mci(graph, node_x, node_y) == result


@pytest.mark.parametrize(
    "node_x,node_y,result",
    [('d', 'e', None)],
)
@build_graph(
    domain={'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'},
    relations=(
        ('a', 'c'),
        ('b', 'c'),
        ('c', 'e'),
        ('c', 'd'),
        ('d', 'f'),
        ('d', 'g'),
        ('e', 'f'),
        ('e', 'g'),
        ('f', 'h'),
        ('g', 'h'),
    ),
)
def test_get_mcs_fail(graph: DiGraph, node_x, node_y, result) -> None:
    assert extract.get_mcs(graph, node_x, node_y) == result


@build_graph(
    domain={2, 4, 5, 6, 7},
    relations={(2, 2), (4, 4), (5, 5), (6, 6), (7, 7)},
)
def test_get_reflexive(graph: DiGraph):
    assert extract.get_reflexive(graph) == {(2, 2), (4, 4), (5, 5), (6, 6),
                                            (7, 7)}


@build_graph(
    domain={2, 4, 5, 6, 7},
    relations={(2, 2), (6, 4), (5, 6), (6, 5), (4, 6)},
)
def test_get_symmetric(graph: DiGraph):
    assert extract.get_symmetric(graph) == {((6, 5), (5, 6)), ((4, 6), (6, 4))}


@build_graph(
    domain={2, 4, 5, 6, 7},
    relations={(2, 2), (5, 4), (5, 6), (6, 5), (7, 7)},
)
def test_get_not_symmetric(graph: DiGraph):
    assert extract.get_not_symmetric(graph) == {((6, 5), (5, 6))}


@build_graph(
    domain={2, 4, 5, 6, 7},
    relations={
        (2, 2),
        (4, 4),
        (5, 4),
        (5, 6),
        (6, 5),
        (4, 5),
        (6, 4),
        (4, 6),
        (5, 5),
        (7, 7),
        (6, 6),
    },
)
def test_get_transitive(graph: DiGraph):
    assert extract.get_transitive(graph) == {
        ((4, 5), (5, 6), (4, 6)),
        ((4, 6), (6, 5), (4, 5)),
        ((5, 4), (4, 6), (5, 6)),
        ((5, 6), (6, 4), (5, 4)),
        ((6, 4), (4, 5), (6, 5)),
        ((6, 5), (5, 4), (6, 4)),
    }
