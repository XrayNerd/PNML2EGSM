from PNML2EGSM.EGSM import Stage
from lxml import etree, objectify


class ProcessFlowGuard:
    parent: Stage
    _tag: str = "processFlowGuard"

    description: str | None
    expression: str | None
    id: str | None
    name: str | None

    def __init__(
        self,
        description: str | None = None,
        expression: str | None = None,
        id: str | None = None,
        name: str | None = None,
    ) -> None:
        self.description = description
        self.expression = expression
        self.id = id
        self.name = name

    def setParent(self, parent: Stage) -> None:
        self.parent = parent

    def toElement(self):
        processFlowGuard = objectify.Element(self._tag)
        objectify.deannotate(
            processFlowGuard,
            pytype=True,
            xsi=True,
            xsi_nil=False,
            cleanup_namespaces=False,
        )
        etree.cleanup_namespaces(processFlowGuard)

        if self.id:
            processFlowGuard.set("id", self.id)
        if self.name:
            processFlowGuard.set("name", self.name)
        if self.expression:
            processFlowGuard.set("expression", self.expression)
        if self.description:
            processFlowGuard.set("description", self.description)

        return processFlowGuard

    def __str__(self) -> str:
        return f"PFG: {self.id=} {self.description=} {self.expression=} {self.name=}"
