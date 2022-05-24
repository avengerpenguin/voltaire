from typing import NamedTuple

from _typeshed import Incomplete

class DeleteNode(NamedTuple):
    node: Incomplete

class InsertNode(NamedTuple):
    target: Incomplete
    tag: Incomplete
    position: Incomplete

class RenameNode(NamedTuple):
    node: Incomplete
    tag: Incomplete

class MoveNode(NamedTuple):
    node: Incomplete
    target: Incomplete
    position: Incomplete

class UpdateTextIn(NamedTuple):
    node: Incomplete
    text: Incomplete

class UpdateTextAfter(NamedTuple):
    node: Incomplete
    text: Incomplete

class UpdateAttrib(NamedTuple):
    node: Incomplete
    name: Incomplete
    value: Incomplete

class DeleteAttrib(NamedTuple):
    node: Incomplete
    name: Incomplete

class InsertAttrib(NamedTuple):
    node: Incomplete
    name: Incomplete
    value: Incomplete

class RenameAttrib(NamedTuple):
    node: Incomplete
    oldname: Incomplete
    newname: Incomplete

class InsertComment(NamedTuple):
    target: Incomplete
    position: Incomplete
    text: Incomplete
