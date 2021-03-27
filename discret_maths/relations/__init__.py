# Standar import
from typing import (
    Callable,
    Iterator,
    Set,
    Tuple,
)
import yaml

# Third imports
from networkx import DiGraph

# Local import
from discret_maths.relations.transform import to_hasse
from discret_maths.relations.extract import (
    get_inverse,
    get_not_symmetric,
    get_not_transitive,
    get_reflexive,
    get_relations,
    get_symmetric,
    get_transitive,
)
from discret_maths.relations.check import (
    is_anti_reflexive,
    is_anti_symmetric,
    is_equivalent,
    is_latice,
    is_not_reflexive,
    is_not_symmetric,
    is_not_transitive,
    is_partial_order,
    is_reflexive,
    is_strict_order,
    is_symmetric,
    is_total_order,
    is_transitive,
)


STRICT: bool = True


def draw_graph(graph: DiGraph, nodes: Set[int]) -> None:
    for node in nodes:
        graph.add_node(node, label=node)


def draw_relation(
    graph: DiGraph,
    relations: Tuple[Tuple[int, int], ...],
    inverse: bool = False,
) -> None:
    for node_x, node_y in relations:
        if inverse:
            graph.add_edge(node_y, node_x, color='blue')
            continue
        graph.add_edge(node_x, node_y, color='blue')


def relations_to_str(relations: Tuple[Tuple[int, int], ...]) -> str:
    result = str()
    for node_x, node_y in relations:
        result += f'({node_x}, {node_y}), '
    return result


def generate_relations(
    nodes: Set[int],
    condition: Callable[[int, int], bool],
    inverse: bool = False,
) -> Iterator[Tuple[int, int]]:
    for node_x in nodes:
        for node_y in nodes:
            if condition(node_x, node_y):
                if inverse:
                    yield (node_y, node_x)
                    continue
                yield (node_x, node_y)


def generate_report(graph: DiGraph) -> None:
    hasse_graph = to_hasse(graph)
    latice = is_latice(hasse_graph)

    report = {
        'relations_type': {
            'reflexive': is_reflexive(graph),
            'anti_reflexive': is_anti_reflexive(graph),
            'not_reflexive': is_not_reflexive(graph),
            'symmetric': is_symmetric(graph),
            'anti_symmetric': is_anti_symmetric(graph),
            'not_symmetric': is_not_symmetric(graph),
            'transitive': is_transitive(graph),
            'not_transitive': is_not_transitive(graph),
            'equivalent': is_equivalent(graph),
            'strict_order': is_strict_order(graph),
            'partial_order': is_partial_order(graph),
            'total_order': is_total_order(graph),
        },
        'relented_nodes': {
            'reflexive': [f'({x}, {y})' for x, y in get_reflexive(graph)],
            'symmetry': [
                f'({a[0]}, {a[1]}), ({b[0]}, {b[1]})'
                for a, b in get_symmetric(graph)
            ],
            'not_symmetric': [
                f'({a[0]}, {a[1]}), ({b[0]}, {b[1]})'
                for a, b in get_not_symmetric(graph)
            ],
            'transitive': [
                f'({x[0]}, {x[1]}), ({y[0]}, {y[1]}), ({z[0]}, {z[1]})'
                for x, y, z in get_transitive(graph)
            ],
            'not_transitive': [
                f'({x[0]}, {x[1]}), ({y[0]}, {y[1]}), ({z[0]}, {z[1]})'
                for x, y, z in get_not_transitive(graph)
            ],
            'inverse':
            relations_to_str(get_inverse(graph)),
            'relations':
            relations_to_str(get_relations(graph)),
        },
        'is_latice': latice
    }

    with open('report.yaml', 'w') as streamer:
        yaml.dump(report, streamer)
