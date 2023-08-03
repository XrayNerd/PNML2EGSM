from PNML2EGSM.EGSM import Stage
from lxml import etree, objectify


class DataFlowGuard:
    parent: Stage
    _tag: str = "dataFlowGuard"

    description: str | None
    eventIds: str | None
    expression: str | None
    id: str | None
    language: str | None
    name: str | None

    def __init__(
        self,
        description: str | None = None,
        eventIds: str | None = None,
        expression: str | None = None,
        id: str | None = None,
        language: str | None = None,
        name: str | None = None,
    ) -> None:
        self.description = description
        self.eventIds = eventIds
        self.expression = expression
        self.id = id
        self.language = language
        self.name = name

    def setParent(self, parent: Stage) -> None:
        self.parent = parent

    def toElement(self):
        dataFlowGuard = objectify.Element(self._tag)
        objectify.deannotate(
            dataFlowGuard,
            pytype=True,
            xsi=True,
            xsi_nil=False,
            cleanup_namespaces=False,
        )
        etree.cleanup_namespaces(dataFlowGuard)

        if self.eventIds:
            dataFlowGuard.set("eventIds", self.eventIds)
        if self.expression:
            dataFlowGuard.set("expression", self.expression)
        if self.id:
            dataFlowGuard.set("id", self.id)
        if self.language:
            dataFlowGuard.set("language", self.language)
        if self.name:
            dataFlowGuard.set("name", self.name)
        if self.description:
            dataFlowGuard.set("description", self.description)

        return dataFlowGuard

    def __str__(self) -> str:
        return f"{self.description=} {self.eventIds=} {self.expression=} {self.id=} {self.language=} {self.name=}"
