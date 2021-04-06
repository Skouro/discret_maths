# Standar import
import itertools
# Third imports
from networkx import DiGraph
import networkx as nx

# Local imports
from discret_maths.utils import get_set_combination
from discret_maths.utils.logger import LOGGER


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


def is_bounded(graph: DiGraph) -> bool:
    first = False
    last = False
    for node in graph.nodes:
        if not nx.ancestors(graph, node):
            first = True
            break

    for node in graph.nodes:
        if not graph.adj[node]:
            last = True
            break

    return first and last


def is_complemented(graph: DiGraph) -> bool:
    from discret_maths.relations import extract

    return all(
        extract.get_complement(graph, node) is not None
        for node in graph.nodes)


def is_distributed(graph: DiGraph) -> bool:
    from discret_maths.relations import extract

    result = list()
    combi = set(itertools.combinations(graph.nodes, 3))
    for n_a, n_b, n_c in combi:
        # n_a . (n_b + n_c)
        mcs_b_c = extract.get_mcs(graph, n_b, n_c)
        _a = extract.get_mci(graph, n_a, mcs_b_c)
        mci_a_b = extract.get_mci(graph, n_a, n_b)
        mci_a_c = extract.get_mci(graph, n_a, n_c)
        # (n_a . n_b) + (n_a . n_c)
        _b = extract.get_mcs(graph, mci_a_b, mci_a_c)
        # n_a . (n_b + n_c) = (n_a . n_b) + (n_a . n_c)
        result.append(_a == _b)
        LOGGER.debug(
            "%s . (%s + %s) = (%s . %s) + (%s . %s)",
            n_a,
            n_b,
            n_c,
            n_a,
            n_b,
            n_a,
            n_c,
        )
        # n_a . mcs_b_c = mci_a_b + mci_a_c
        LOGGER.debug(
            "%s . %s = %s + %s",
            n_a,
            mcs_b_c,
            mci_a_b,
            mci_a_c,
        )
        LOGGER.debug(
            "%s = %s",
            _a,
            _b,
        )

    return all(result)


def is_booblean_algebra(graph: DiGraph) -> bool:
    return is_complemented(graph) and is_distributed(graph)
