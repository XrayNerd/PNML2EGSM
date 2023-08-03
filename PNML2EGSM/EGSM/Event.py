from PNML2EGSM.EGSM import EventModel
from lxml import objectify, etree


class Event:
    parent: EventModel
    _tag: str = "event"

    description: str
    id: str
    name: str

    def __init__(
        self,
        description: str | None = None,
        id: str | None = None,
        name: str | None = None,
    ) -> None:
        self.description = description
        self.id = id
        self.name = name

    def setParent(self, parent: EventModel) -> None:
        self.parent = parent

    def toElement(self):
        event = objectify.Element(self._tag)
        objectify.deannotate(
            event, pytype=True, xsi=True, xsi_nil=False, cleanup_namespaces=False
        )
        etree.cleanup_namespaces(event)

        if self.id:
            event.set("id", self.id)
        if self.name:
            event.set("name", self.name)
        if self.description:
            event.set("description", self.description)

        return event

    def __str__(self) -> str:
        return f"Event: {self.description=} {self.id=} {self.name=}"
