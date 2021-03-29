# pylint:disable=unused-argument

from test.relations import build_graph
from networkx.classes.digraph import DiGraph
from discret_maths.relations import draw_relation, relations_to_str


@build_graph(
    domain={2, 4, 5, 6, 7},
    relations={
        (2, 2),
        (4, 4),
    },
)
def test_relations_to_str(graph: DiGraph) -> None:
    assert relations_to_str(graph.edges) == "(2, 2), (4, 4), "


def test_draw_relations(graph: DiGraph) -> None:
    relations = {(2, 2), (4, 4), (5, 4), (5, 6)}
    draw_relation(graph, relations)
    assert relations == set((x, y) for x, y in graph.edges)
