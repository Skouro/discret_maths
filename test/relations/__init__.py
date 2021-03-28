# pylint:disable=unused-argument

import functools
from typing import (
    Any,
    Callable,
    Optional,
    Set,
    Tuple,
    TypeVar,
    cast,
)
from networkx import DiGraph
from discret_maths.relations import (
    draw_graph,
    draw_relation,
)
TFun = TypeVar('TFun', bound=Callable[..., Any])


def build_graph(
    domain: Optional[Set[Any]] = None,
    relations: Optional[Set[Tuple[Any, Any]]] = None,
) -> Callable[[TFun], TFun]:
    def decorator(function: TFun) -> TFun:
        @functools.wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            graph = DiGraph()
            draw_graph(graph, domain or kwargs['domain'])
            draw_relation(graph, relations or kwargs['relations'])
            kwargs['graph'] = graph
            return function(*args, **kwargs)

        return cast(TFun, wrapper)

    return decorator
