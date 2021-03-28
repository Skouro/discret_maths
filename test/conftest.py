from networkx.classes.digraph import DiGraph
import pytest


@pytest.fixture
def graph() -> DiGraph:
    yield DiGraph()
