# Standar import
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
)
import math
from contextlib import suppress

# Third import
from networkx import DiGraph
from networkx.algorithms.shortest_paths.generic import all_shortest_paths
from networkx.exception import NetworkXNoPath
import networkx as nx

# Local import
from discret_maths.relations import check
from discret_maths.utils.logger import LOGGER
from discret_maths.utils import get_set_combination

# Constants
STRICT: bool = True


def get_reflexive(
    graph: DiGraph,
    strict: bool = STRICT,
) -> Set[Tuple[int, int]]:
    nodes = graph.nodes
    if strict and not check.is_reflexive(graph):
        return set()
    return set((node, node) for node in nodes if graph.has_edge(node, node))


def get_symmetric(
    graph: DiGraph,
    strict: bool = STRICT,
) -> Set[Tuple[Tuple[int, int], Tuple[int, int]]]:
    if strict and not check.is_symmetric(graph):
        return set()

    result = set()
    analyzed = set()
    for n_x, n_y in graph.edges:
        if n_x == n_y:
            continue
        if (graph.has_edge(n_x, n_y) and graph.has_edge(n_y, n_x)
                and (n_x, n_y) not in analyzed and (n_y, n_x) not in analyzed):
            result.add(((n_x, n_y), (n_y, n_x)))
            analyzed.add((n_x, n_y))
            analyzed.add((n_y, n_x))

    return result


def get_not_symmetric(
    graph: DiGraph,
    strict: bool = STRICT,
) -> Set[Tuple[Tuple[int, int], Tuple[int, int]]]:
    if strict and not check.is_not_symmetric(graph):
        return set()

    return get_symmetric(graph, False)


def get_transitive(
    graph: DiGraph,
    strict: bool = STRICT
) -> Set[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
    if strict and not check.is_transitive(graph):
        return set()

    return set(((x, y), (y, z), (x, z)) for x, y in graph.edges
               if x != y and graph.has_edge(x, y) for z in graph.adj[y]
               if y != z and graph.has_edge(x, z))


def get_not_transitive(
    graph: DiGraph,
    strict: bool = STRICT,
) -> Set[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
    if strict and not check.is_not_transitive(graph):
        return set()

    return set(((x, y), (y, z), (x, z)) for x, y in graph.edges
               if x != y and graph.has_edge(x, y) for z in graph.adj[y]
               if y != z and not graph.has_edge(x, z))


def get_inverse(graph: DiGraph, ) -> Tuple[Tuple[int, int], ...]:
    return tuple((y, x) for x, y in graph.edges)


def get_relations(graph: DiGraph, ) -> Tuple[Tuple[int, int], ...]:

    return tuple((x, y) for x, y in graph.edges)


def math_get_mci(graph: DiGraph, node_x: int, node_y: int) -> Optional[int]:
    # maxima cuota inferior
    mci = math.gcd(node_x, node_y)
    return mci if graph.has_node(mci) else None


def math_get_mcs(graph: DiGraph, node_x: int, node_y: int) -> Optional[int]:
    # minima cuota superior
    mci = math.lcm(node_x, node_y)
    return mci if graph.has_node(mci) else None


def _recursive_pred(graph: DiGraph, node: Any) -> Iterator[Any]:
    for pred in graph.pred[node].keys():
        if pred == node:
            continue
        yield pred
        yield from _recursive_pred(graph, pred)


def _recursive_adj(graph: DiGraph, node: Any) -> Iterator[Any]:
    for pred in graph.adj[node].keys():
        if pred == node:
            continue
        yield pred
        yield from (_recursive_adj(graph, pred))


def get_avg_lent_paths(paths: Tuple[List[Any], ...]) -> float:
    lengths = tuple(len(path) for path in paths)
    return sum(lengths) / len(paths)


def get_cs(graph: DiGraph, node_x: Any, node_y: Any) -> Set[Any]:
    x_adj = set(_recursive_adj(graph, node_x))
    y_adj = set(_recursive_adj(graph, node_y))
    result = x_adj.intersection(y_adj)
    with suppress(NetworkXNoPath):
        if tuple(all_shortest_paths(graph, node_x, node_y)):
            result.add(node_y)
    with suppress(NetworkXNoPath):
        if tuple(all_shortest_paths(graph, node_y, node_x)):
            result.add(node_x)
    return result


def get_ci(graph: DiGraph, node_x: Any, node_y: Any) -> Set[Any]:
    x_pred = set(_recursive_pred(graph, node_x))
    y_pred = set(_recursive_pred(graph, node_y))
    result = x_pred.intersection(y_pred)
    with suppress(NetworkXNoPath):
        if tuple(all_shortest_paths(graph, node_x, node_y)):
            result.add(node_x)
    with suppress(NetworkXNoPath):
        if tuple(all_shortest_paths(graph, node_y, node_x)):
            result.add(node_y)
    return result


def get_all_cs(graph: DiGraph) -> Iterator[Tuple[Set[Any], Set[Any]]]:
    for node_x, node_y in get_set_combination(graph.nodes):
        yield ({node_x, node_y}, get_cs(graph, node_x, node_y))


def get_all_ci(graph: DiGraph) -> Iterator[Tuple[Set[Any], Set[Any]]]:
    for node_x, node_y in get_set_combination(graph.nodes):
        yield ({node_x, node_y}, get_ci(graph, node_x, node_y))


def _get_mci(graph: DiGraph, node_x: Any, node_y: Any) -> Optional[Any]:
    with suppress(NetworkXNoPath):
        if tuple(all_shortest_paths(graph, node_x, node_y)):
            return {node_x}
    with suppress(NetworkXNoPath):
        if tuple(all_shortest_paths(graph, node_y, node_x)):
            return {node_y}

    x_pred = set(_recursive_pred(graph, node_x))
    y_pred = set(_recursive_pred(graph, node_y))

    adj_common = x_pred.intersection(y_pred)

    short_common_pred: List[Tuple[Any, float]] = list()
    for node in adj_common:
        x_to_node = tuple(all_shortest_paths(graph, node, node_x))
        avg_x = get_avg_lent_paths(x_to_node)
        y_to_node = tuple(all_shortest_paths(graph, node, node_y))
        avg_y = get_avg_lent_paths(y_to_node)

        tow_paths_length = avg_x + avg_y
        if not short_common_pred:
            short_common_pred = [(node, avg_x + avg_y)]
        elif tow_paths_length == short_common_pred[0][1]:
            short_common_pred.append((node, tow_paths_length))
        elif tow_paths_length < short_common_pred[0][1]:
            short_common_pred = [(node, tow_paths_length)]

    return {node for node, _ in short_common_pred}


def _get_mcs(graph: DiGraph, node_x: Any, node_y: Any) -> Optional[Any]:
    with suppress(NetworkXNoPath):
        if tuple(all_shortest_paths(graph, node_x, node_y)):
            return {node_y}
    with suppress(NetworkXNoPath):
        if tuple(all_shortest_paths(graph, node_y, node_x)):
            return {node_x}

    adj_common = set(_recursive_adj(graph, node_x)).intersection(
        set(_recursive_adj(graph, node_y)))

    short_common_adj: List[Tuple[Any, float]] = list()
    for node in adj_common:
        x_to_node = tuple(all_shortest_paths(graph, node_x, node))
        avg_x = get_avg_lent_paths(x_to_node)
        y_to_node = tuple(all_shortest_paths(graph, node_y, node))
        avg_y = get_avg_lent_paths(y_to_node)

        tow_paths_length = avg_x + avg_y
        if not short_common_adj:
            short_common_adj = [(node, avg_x + avg_y)]
        elif tow_paths_length == short_common_adj[0][1]:
            short_common_adj.append((node, tow_paths_length))
        elif tow_paths_length < short_common_adj[0][1]:
            short_common_adj = [(node, tow_paths_length)]

    return {node for node, _ in short_common_adj}


def get_all_mci(graph: DiGraph) -> Iterator[Tuple[Set[Any], Any]]:
    for node_x, node_y in get_set_combination(graph.nodes):
        yield ({node_x, node_y}, _get_mci(graph, node_x, node_y))


def get_all_mcs(graph: DiGraph) -> Iterator[Tuple[Set[Any], Any]]:
    for node_x, node_y in get_set_combination(graph.nodes):
        yield ({node_x, node_y}, _get_mcs(graph, node_x, node_y))


def get_mci(graph: DiGraph, node_x: Any, node_y: Any) -> Optional[Any]:
    # maxima cuota inferior

    bounds = _get_mci(graph, node_x, node_y)
    if not bounds:
        LOGGER.warning(
            'nodes %s and %s have no maximum lower cote',
            node_x,
            node_y,
        )
        return None

    if len(bounds) > 1:
        LOGGER.warning(
            'nodes %s and %s have more than one maximum lower cote: %s',
            node_x,
            node_y,
            bounds,
        )
        return None

    return bounds.pop()


def get_mcs(graph: DiGraph, node_x: Any, node_y: Any) -> Optional[Any]:
    # minima cuota superior
    bounds = _get_mcs(graph, node_x, node_y)
    if not bounds:
        LOGGER.warning(
            'nodes %s and %s have no upper minimum quota',
            node_x,
            node_y,
        )
        return None

    if len(bounds) > 1:
        LOGGER.warning(
            'nodes %s and %s has more than one higher minimum quota: %s',
            node_x,
            node_y,
            bounds,
        )
        return None

    return bounds.pop()


def get_bounded(graph: DiGraph) -> Tuple[Any, Any]:
    first = None
    last = None
    for node in graph.nodes:
        if not nx.ancestors(graph, node):
            first = node
            break

    for node in graph.nodes:
        if not graph.adj[node]:
            last = node
            break

    return (first, last)


def get_complement(graph: DiGraph, node: Any) -> Optional[Any]:
    minimum, maximum = get_bounded(graph)

    for _node in graph.nodes:
        if node == _node:
            continue
        mcs = get_mcs(graph, node, _node)
        mci = get_mci(graph, node, _node)
        if mcs == maximum and mci == minimum:
            return _node

    LOGGER.info(" %s + %s = %s", node, _node, mcs)
    LOGGER.info(" %s . %s = %s", node, _node, mci)

    return None


def get_complements(graph: DiGraph) -> Dict[Any, Optional[Any]]:
    return {node: get_complement(graph, node) for node in graph.nodes}
