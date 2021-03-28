# Standar import

# Third imports
from typing import Optional, Set
from networkx import DiGraph

# Local imports
from discret_maths.utils import get_set_combination


def is_reflexive(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
) -> bool:
    nodes = nodes or graph.nodes
    return all(graph.has_edge(node, node) for node in nodes)


def is_anti_reflexive(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
) -> bool:
    nodes = nodes or graph.nodes
    return all(not graph.has_edge(node, node) for node in nodes)


def is_not_reflexive(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
) -> bool:
    nodes = nodes or graph.nodes
    if is_reflexive(graph, nodes):
        return False
    return any(graph.has_edge(node, node) for node in nodes)


def is_symmetric(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
) -> bool:
    nodes = nodes or graph.nodes
    return all(
        graph.has_edge(y, x) for x, y in get_set_combination(nodes)
        if x != y and graph.has_edge(x, y))


def is_anti_symmetric(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
) -> bool:
    nodes = nodes or graph.nodes
    return all(not graph.has_edge(y, x) for x, y in get_set_combination(nodes)
               if x != y if graph.has_edge(x, y))


def is_not_symmetric(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
) -> bool:
    nodes = nodes or graph.nodes

    if is_symmetric(graph, nodes):
        return False

    return any(
        graph.has_edge(y, x) and graph.has_edge(x, y)
        for x, y in get_set_combination(nodes) if x != y)


def is_transitive(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
) -> bool:
    nodes = nodes or graph.nodes
    return all(
        graph.has_edge(x, z) for x, y in get_set_combination(nodes)
        if x != y and graph.has_edge(x, y) for z in graph.adj[y] if y != z)


def is_not_transitive(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
) -> bool:
    nodes = nodes or graph.nodes
    return any(not graph.has_edge(x, z) for x, y in get_set_combination(nodes)
               if x != y and graph.has_edge(x, y) for z in graph.adj[y]
               if y != z)


def is_equivalent(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
) -> bool:
    nodes = nodes or graph.nodes
    reflexive = is_reflexive(graph, nodes)
    symmetric = is_symmetric(graph, nodes)
    transitive = is_transitive(graph, nodes)

    return reflexive and symmetric and transitive


def is_strict_order(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
) -> bool:
    nodes = nodes or graph.nodes
    transitive = is_transitive(graph, nodes)
    anti = is_anti_symmetric(graph, nodes)

    return anti and transitive


def is_partial_order(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
) -> bool:
    nodes = nodes or graph.nodes
    reflexive = is_reflexive(graph, nodes)
    anti_symmetric = is_anti_symmetric(graph, nodes)
    transitive = is_transitive(graph, nodes)

    return reflexive and anti_symmetric and transitive


def is_total_order(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
) -> bool:
    nodes = nodes or graph.nodes

    reflexive = is_reflexive(graph, nodes)
    anti_symmetric = is_anti_symmetric(graph, nodes)
    transitive = is_transitive(graph, nodes)
    all_relatione = all(
        graph.has_edge(x, y) and graph.has_edge(y, x)
        for x, y in get_set_combination(nodes))

    return reflexive and anti_symmetric and transitive and all_relatione
