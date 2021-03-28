# Standar import
from typing import (
    Any,
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

# Local import
from discret_maths.relations import check
from discret_maths.utils.logger import LOGGER

# Constants
STRICT: bool = True


def get_reflexive(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
    strict: bool = STRICT,
) -> Tuple[Tuple[int, int], ...]:
    nodes = nodes or graph.nodes
    if strict and not check.is_reflexive(graph, nodes):
        return tuple()
    return tuple((node, node) for node in nodes if graph.has_edge(node, node))


def get_symmetric(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
    strict: bool = STRICT,
) -> Tuple[Tuple[Tuple[int, int], Tuple[int, int]], ...]:
    nodes = nodes or graph.nodes
    if strict and not check.is_symmetric(graph, nodes):
        return tuple()
    return tuple(((x, y), (y, x)) for x in nodes for y in nodes
                 if x != y and graph.has_edge(x, y) and graph.has_edge(y, x))


def get_not_symmetric(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
    strict: bool = STRICT,
) -> Tuple[Tuple[Tuple[int, int], Tuple[int, int]], ...]:
    nodes = nodes or graph.nodes
    if strict and not check.is_not_symmetric(graph, nodes):
        return tuple()

    return get_symmetric(graph, nodes, False)


def get_transitive(
    graph: DiGraph,
    nodes: Optional[Set[int]] = None,
    strict: bool = STRICT
) -> Tuple[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]], ...]:
    nodes = nodes or graph.nodes
    if strict and not check.is_transitive(graph, nodes):
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
    if strict and not check.is_not_transitive(graph, nodes):
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
        yield pred
        yield from (_recursive_pred(graph, pred))


def _recursive_adj(graph: DiGraph, node: Any) -> Iterator[Any]:
    for pred in graph.adj[node].keys():
        yield pred
        yield from (_recursive_adj(graph, pred))


def get_avg_lent_paths(paths: Tuple[List[Any], ...]) -> float:
    lengths = (len(path) for path in paths)
    return sum(lengths) / len(paths)


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


def get_mci(graph: DiGraph, node_x: Any, node_y: Any) -> Optional[Any]:
    # maxima cuota inferior

    cotes = _get_mci(graph, node_x, node_y)
    if not cotes:
        LOGGER.warning(
            'nodes %s and %s have no maximum lower cote',
            node_x,
            node_y,
        )
        return None

    if len(cotes) > 1:
        LOGGER.warning(
            'nodes %s and %s have more than one maximum lower cote: %s',
            node_x,
            node_y,
            cotes,
        )
        return None

    return cotes.pop()


def get_mcs(graph: DiGraph, node_x: Any, node_y: Any) -> Optional[Any]:
    # minima cuota superior
    cotes = _get_mcs(graph, node_x, node_y)
    if not cotes:
        LOGGER.warning(
            'nodes %s and %s have no upper minimum quota',
            node_x,
            node_y,
        )
        return None

    if len(cotes) > 1:
        LOGGER.warning(
            'nodes %s and %s has more than one higher minimum quota: %s',
            node_x,
            node_y,
            cotes,
        )
        return None

    return cotes.pop()
