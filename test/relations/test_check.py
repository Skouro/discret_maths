# pylint:disable=unused-argument
# type: ignore

from test.relations import build_graph
import pytest
from networkx.classes.digraph import DiGraph
from discret_maths.relations import (
    draw_graph,
    draw_relation,
)
from discret_maths.relations import check


@pytest.mark.parametrize("domain,relations", [
    ({2, 4, 5, 6, 7}, {(2, 2), (4, 4), (5, 5), (6, 6), (7, 7)}),
])
@build_graph()
def test_reflexive(graph: DiGraph, domain, relations) -> None:
    assert check.is_reflexive(graph)


@pytest.mark.parametrize("domain,relations", [
    ({2, 4, 5, 6, 7}, {(2, 2), (4, 2), (5, 5), (6, 6), (7, 6)}),
])
@build_graph()
def test_reflexive_false(graph: DiGraph, domain, relations) -> None:
    assert not check.is_reflexive(graph)


@pytest.mark.parametrize("domain,relations", [
    ({2, 4, 5, 6, 7}, {(4, 5), (2, 4), (5, 2), (6, 7), (7, 6)}),
])
@build_graph()
def test_anti_reflexive(graph: DiGraph, domain, relations) -> None:
    assert check.is_anti_reflexive(graph)


@pytest.mark.parametrize("domain,relations", [
    ({2, 4, 5, 6, 7}, {(4, 5), (2, 2), (5, 2), (6, 6), (7, 6)}),
])
@build_graph()
def test_anti_reflexive_false(graph: DiGraph, domain, relations) -> None:
    assert not check.is_anti_reflexive(graph)


@pytest.mark.parametrize("domain,relations", [
    ({2, 4, 5, 6, 7}, {(2, 2), (4, 4), (5, 6), (6, 5), (7, 7)}),
])
@build_graph()
def test_not_reflexive(graph: DiGraph, domain, relations) -> None:
    assert check.is_not_reflexive(graph)

    graph = DiGraph()
    relations = {(4, 4), (2, 2), (5, 5), (6, 6), (7, 7)}
    draw_graph(graph, domain)
    draw_relation(graph, relations)
    assert not check.is_not_reflexive(graph)


@pytest.mark.parametrize("domain,relations", [
    ({2, 4, 5, 6, 7}, {(4, 4), (2, 2), (5, 5), (6, 6), (7, 7)}),
])
@build_graph()
def test_not_reflexive_false(graph: DiGraph, domain, relations) -> None:
    assert not check.is_not_reflexive(graph)


@pytest.mark.parametrize("domain,relations", [
    ({2, 4, 5, 6, 7}, {(2, 2), (6, 4), (5, 6), (6, 5), (4, 6)}),
])
@build_graph()
def test_symmetric(graph: DiGraph, domain, relations) -> None:
    assert check.is_symmetric(graph)


@pytest.mark.parametrize("domain,relations", [
    ({2, 4, 5, 6, 7}, {(2, 2), (2, 6), (6, 4), (5, 6), (5, 4), (6, 5),
                       (4, 6)}),
])
@build_graph()
def test_symmetric_false(graph: DiGraph, domain, relations) -> None:
    assert not check.is_symmetric(graph)


@pytest.mark.parametrize("domain,relations", [
    ({2, 4, 5, 6, 7}, {(2, 2), (6, 4), (5, 6), (6, 2), (4, 5), (7, 7)}),
])
@build_graph()
def test_anti_symmetric(graph: DiGraph, domain, relations) -> None:
    assert check.is_anti_symmetric(graph)


@pytest.mark.parametrize("domain,relations", [
    ({2, 4, 5, 6, 7}, {(2, 2), (6, 4), (5, 6), (6, 2), (2, 6), (4, 5),
                       (7, 7)}),
])
@build_graph()
def test_anti_symmetric_false(graph: DiGraph, domain, relations) -> None:
    assert not check.is_anti_symmetric(graph)
