from PNML2EGSM.EGSM import Event, DocumentRoot
from lxml import objectify, etree


class EventModel:
    parent: DocumentRoot
    _namespace: str = "http://siena.ibm.com/model/CompositeApplication"
    _tag: str = "EventModel"

    description: str
    id: str
    name: str

    events: list

    def __init__(
        self,
        description: str | None = None,
        id: str | None = None,
        name: str | None = None,
    ) -> None:
        self.description = description
        self.id = id
        self.name = name

        self.events = []

    def setParent(self, parent: DocumentRoot) -> None:
        self.parent = parent

    def addEvent(self, event: Event) -> None:
        self.events.append(event)
        event.setParent(self)

    def toElement(self):
        tag = etree.QName(self._namespace, self._tag)
        eventModel = objectify.Element(tag)
        objectify.deannotate(
            eventModel, pytype=True, xsi=True, xsi_nil=False, cleanup_namespaces=False
        )
        etree.cleanup_namespaces(eventModel)

        if self.id:
            eventModel.set("id", self.id)
        if self.name:
            eventModel.set("name", self.name)
        if self.description:
            eventModel.set("description", self.description)

        for event in self.events:
            eventModel.append(event.toElement())

        return eventModel

    def __str__(self) -> str:
        return f"Event: {self.description=} {self.id=} {self.name=}"
