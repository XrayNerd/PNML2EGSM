from PNML2EGSM.EGSM import Component, EventModel
from lxml.builder import ElementMaker


class DocumentRoot:
    version: str | None

    kwargs: dict

    namespaces = {
        "xmi": "http://www.omg.org/XMI",
        "application": "http://siena.ibm.com/model/CompositeApplication",
    }

    component: Component = None
    eventModel: EventModel = None

    def __init__(self, *args, **kwargs) -> None:
        self.kwargs = kwargs

        self.component = None
        self.eventModel = None

    def addComponent(self, component: Component) -> None:
        self.component = component
        component.setParent(self)

    def addEventModel(self, eventModel: EventModel) -> None:
        self.eventModel = eventModel
        eventModel.setParent(self)

    def toElement(self):
        documentRoot = ElementMaker(
            namespace=self.namespaces["xmi"], nsmap=self.namespaces
        )
        documentRoot = documentRoot.CompositeApplicationType()

        if self.kwargs["kwargs"]:
            for key, value in self.kwargs["kwargs"].items():
                documentRoot.set(key, value)
        documentRoot.set("{http://www.omg.org/XMI}version", "2.0")

        if self.eventModel:
            documentRoot.append(self.eventModel.toElement())
        if self.component:
            documentRoot.append(self.component.toElement())

        return documentRoot
