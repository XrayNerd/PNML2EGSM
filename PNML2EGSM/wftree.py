from enum import Enum
from typing import Optional, Union


class RPSTType(Enum):
    TRIVIAL = 1
    POLYGON = 2
    BOND = 3
    RIGID = 4


class WFTreeRefinedType(Enum):
    UNDEFINED = 1
    PLACE_BORDERED = 2
    TRANSITION_BORDERED = 3
    LOOP = 4


class RPST:
    pass


class Node:
    _parent = None
    type: RPSTType
    refinedType: WFTreeRefinedType

    source: str | None = None
    dest: str | None = None
    children = []

    places = []
    transitions = []


class Fragment:
    _parent = ""
    _id: str = ""

    # Fragment RPST Type
    type: RPSTType

    # Refined Workflow Tree Type for Bonds
    refinedType: WFTreeRefinedType | None

    # Identifier for Entry
    entry: str

    # Identifier for Exit
    exit_: str

    nodes: list = []

    children: list = []

    def __init__(
        self,
        entry: str,
        exit_: str,
        nodes: list,
        type_: RPSTType,
        refinedType: WFTreeRefinedType,
        id_: str = "",
    ) -> None:
        self.entry = entry
        self.exit_ = exit_
        self.nodes = nodes
        self.type_ = type_
        self.refinedType = refinedType
        self._id = id_
        self.children = []

    def __str__(self) -> str:
        return f"{self._id} {self.entry} {self.exit_} {self.type_} {self.refinedType}"

    def getId(self) -> str:
        return self._id

    def setParent(self, parent) -> None:
        self._parent = parent

    def addChild(self, child) -> None:
        if child not in self.children:
            self.children.append(child)
            child.setParent(self)


def get_fragment_depth(fragment: Fragment, depth: int = 0) -> int:
    if not isinstance(fragment._parent, Fragment):
        return depth
    else:
        return get_fragment_depth(fragment=fragment._parent, depth=depth + 1)


def getChildTree(fragment: Fragment, indent=""):
    print(f"{indent}{fragment}")
    for child in fragment.children:
        getChildTree(child, indent=indent + "  ")


def parse_nodes(file_in: str) -> tuple[dict[str, Fragment], Optional[Fragment]]:
    fragments: dict[str, Fragment] = {}
    relationships: dict[str, str] = {}
    with open(file=file_in, mode="r") as f:
        for line in f:
            # a = line.strip().split(",")
            refinedType, name, type_, entry, exit_, parent, *nodes = (
                line.strip().replace("[", "").replace("]", "").split(",")
            )
            refined_nodes = []
            for pair in nodes:
                first, second = pair.strip().split("->")
                refined_nodes.append((first, second))
            fragment = Fragment(
                entry=entry,
                exit_=exit_,
                nodes=refined_nodes,
                type_=RPSTType[type_],
                refinedType=WFTreeRefinedType[refinedType],
                id_=name,
            )
            fragments[fragment.getId()] = fragment
            relationships[fragment.getId()] = parent
    root: Optional[Fragment] = None
    for child, parent in relationships.items():
        if parent != "None":
            fragments[parent].addChild(fragments[child])
        else:
            root = fragments[child]
    return fragments, root
