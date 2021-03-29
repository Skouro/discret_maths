# Standar import

# Third imports
from networkx import DiGraph

# Local imports
from discret_maths.utils import get_set_combination


def is_reflexive(graph: DiGraph) -> bool:
    return all(graph.has_edge(node, node) for node in graph.nodes)


def is_anti_reflexive(graph: DiGraph) -> bool:
    return all(not graph.has_edge(node, node) for node in graph.nodes)


def is_not_reflexive(graph: DiGraph) -> bool:
    if is_reflexive(graph):
        return False
    return any(graph.has_edge(node, node) for node in graph.nodes)


def is_symmetric(graph: DiGraph) -> bool:
    return all(
        graph.has_edge(y, x) for x, y in graph.edges
        if x != y and graph.has_edge(x, y))


def is_anti_symmetric(graph: DiGraph) -> bool:
    return all(not graph.has_edge(y, x) for x, y in graph.edges if x != y
               if graph.has_edge(x, y))


def is_not_symmetric(graph: DiGraph) -> bool:
    if is_symmetric(graph):
        return False

    return any(
        graph.has_edge(y, x) and graph.has_edge(x, y) for x, y in graph.edges
        if x != y)


def is_transitive(graph: DiGraph) -> bool:
    return all(
        graph.has_edge(x, z) for x, y in get_set_combination(graph.nodes)
        if x != y and graph.has_edge(x, y) for z in graph.adj[y] if y != z)


def is_not_transitive(graph: DiGraph) -> bool:
    return any(not graph.has_edge(x, z)
               for x, y in get_set_combination(graph.nodes)
               if x != y and graph.has_edge(x, y) for z in graph.adj[y]
               if y != z)


def is_equivalent(graph: DiGraph) -> bool:
    reflexive = is_reflexive(graph)
    symmetric = is_symmetric(graph)
    transitive = is_transitive(graph)

    return reflexive and symmetric and transitive


def is_strict_order(graph: DiGraph) -> bool:
    transitive = is_transitive(graph)
    anti = is_anti_symmetric(graph)

    return anti and transitive


def is_partial_order(graph: DiGraph) -> bool:
    reflexive = is_reflexive(graph)
    anti_symmetric = is_anti_symmetric(graph)
    transitive = is_transitive(graph)

    return reflexive and anti_symmetric and transitive


def is_total_order(graph: DiGraph) -> bool:
    reflexive = is_reflexive(graph)
    anti_symmetric = is_anti_symmetric(graph)
    transitive = is_transitive(graph)
    all_relatione = all(
        graph.has_edge(x, y) and graph.has_edge(y, x)
        for x, y in get_set_combination(graph.nodes))

    return reflexive and anti_symmetric and transitive and all_relatione
