from collections.abc import Generator

from _typeshed import Incomplete
from xmldiff import actions as actions
from xmldiff import utils as utils

class Differ:
    F: Incomplete
    uniqueattrs: Incomplete
    fast_match: Incomplete
    def __init__(
        self,
        F: Incomplete | None = ...,
        uniqueattrs: Incomplete | None = ...,
        ratio_mode: str = ...,
        fast_match: bool = ...,
    ) -> None: ...
    left: Incomplete
    right: Incomplete
    def clear(self) -> None: ...
    def set_trees(self, left, right) -> None: ...
    def append_match(self, lnode, rnode, max_match) -> None: ...
    def match(
        self, left: Incomplete | None = ..., right: Incomplete | None = ...
    ): ...
    def node_ratio(self, left, right): ...
    def node_text(self, node): ...
    def leaf_ratio(self, left, right): ...
    def child_ratio(self, left, right): ...
    def update_node_tag(
        self, left, right
    ) -> Generator[Incomplete, None, None]: ...
    def update_node_attr(
        self, left, right
    ) -> Generator[Incomplete, None, None]: ...
    def update_node_text(
        self, left, right
    ) -> Generator[Incomplete, None, None]: ...
    def find_pos(self, node): ...
    def align_children(
        self, left, right
    ) -> Generator[Incomplete, None, Incomplete]: ...
    def diff(
        self, left: Incomplete | None = ..., right: Incomplete | None = ...
    ) -> Generator[Incomplete, None, None]: ...
