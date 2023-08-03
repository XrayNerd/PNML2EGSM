from PNML2EGSM.EGSM import Stage
from lxml import etree, objectify


class FaultLogger:
    parent: Stage
    _tag: str = "faultLogger"

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
        faultLogger = objectify.Element(self._tag)
        objectify.deannotate(
            faultLogger, pytype=True, xsi=True, xsi_nil=False, cleanup_namespaces=False
        )
        etree.cleanup_namespaces(faultLogger)

        if self.eventIds:
            faultLogger.set("eventIds", self.eventIds)
        if self.expression:
            faultLogger.set("expression", self.expression)
        if self.id:
            faultLogger.set("id", self.id)
        if self.language:
            faultLogger.set("language", self.language)
        if self.name:
            faultLogger.set("name", self.name)
        if self.description:
            faultLogger.set("description", self.description)

        return faultLogger

    def __str__(self) -> str:
        return f"FL: {self.description=} {self.eventIds=} {self.expression=} {self.id=} {self.language=} {self.name=}"
