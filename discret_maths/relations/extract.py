# Standar import
from typing import (
    Optional,
    Set,
    Tuple,
)

# Third import
from networkx import DiGraph

# Local import
from discret_maths.relations.check import (
    is_not_symmetric,
    is_not_transitive,
    is_reflexive,
    is_symmetric,
    is_transitive,
)

# Constants
STRICT: bool = True


def get_reflexive(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
    strict: bool = STRICT,
) -> Tuple[Tuple[int, int], ...]:
    nodes = nodes or graph.nodes
    if strict and not is_reflexive(graph, nodes):
        return tuple()
    return tuple((node, node) for node in nodes if graph.has_edge(node, node))


def get_symmetric(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
    strict: bool = STRICT,
) -> Tuple[Tuple[Tuple[int, int], Tuple[int, int]], ...]:
    nodes = nodes or graph.nodes
    if strict and not is_symmetric(graph, nodes):
        return tuple()
    return tuple(((x, y), (y, x)) for x in nodes for y in nodes
                 if x != y and graph.has_edge(x, y) and graph.has_edge(y, x))


def get_not_symmetric(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
    strict: bool = STRICT,
) -> Tuple[Tuple[Tuple[int, int], Tuple[int, int]], ...]:
    nodes = nodes or graph.nodes
    if strict and not is_not_symmetric(graph, nodes):
        return tuple()

    return get_symmetric(graph, nodes, False)


def get_transitive(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
    strict: bool = STRICT
) -> Tuple[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]], ...]:
    nodes = nodes or graph.nodes
    if strict and not is_transitive(graph, nodes):
        return tuple()

    return tuple(((x, y), (y, z), (x, z)) for x in nodes for y in nodes
                 if x != y and graph.has_edge(x, y) for z in graph.adj[y]
                 if y != z and graph.has_edge(x, z))


def get_not_transitive(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
    strict: bool = STRICT,
) -> Tuple[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]], ...]:
    nodes = nodes or graph.nodes
    if strict and not is_not_transitive(graph, nodes):
        return tuple()

    return tuple(((x, y), (y, z), (x, z)) for x in nodes for y in nodes
                 if x != y and graph.has_edge(x, y) for z in graph.adj[y]
                 if y != z and not graph.has_edge(x, z))


def get_inverse(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
) -> Tuple[Tuple[int, int], ...]:
    nodes = nodes or graph.nodes

    return tuple((y, x) for x in nodes for y in nodes if graph.has_edge(x, y))


def get_relations(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
) -> Tuple[Tuple[int, int], ...]:
    nodes = nodes or graph.nodes

    return tuple((x, y) for x in nodes for y in nodes if graph.has_edge(x, y))
