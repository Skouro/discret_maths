# Standar import
from contextlib import suppress

# Third import
from networkx import DiGraph
from networkx.exception import NetworkXError

# Local import
from discret_maths.relations.extract import (
    get_reflexive,
    get_transitive,
)


def to_hasse(graph: DiGraph) -> DiGraph:
    _graph = graph.copy()
    for pair_x, _, pair_z in get_transitive(_graph):
        node_x, _ = pair_x
        _, node_z = pair_z
        with suppress(NetworkXError):
            _graph.remove_edge(node_x, node_z)
    for node_x, node_y in get_reflexive(_graph):
        _graph.remove_edge(node_x, node_y)

    return _graph
