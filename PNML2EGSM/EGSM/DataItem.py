from PNML2EGSM.EGSM import InformationModel
from lxml import objectify, etree


class DataItem:
    parent: InformationModel
    _tag: str = "dataItem"

    id: str
    listElement: str
    rootElement: str
    schemaUri: str

    def __init__(
        self,
        id: str | None = None,
        listElement: str | None = None,
        rootElement: str | None = None,
        schemaUri: str | None = None,
    ) -> None:
        self.id = id
        self.listElement = listElement
        self.rootElement = rootElement
        self.schemaUri = schemaUri

    def setParent(self, parent: InformationModel) -> None:
        self.parent = parent

    def toElement(self):
        dataItem = objectify.Element(self._tag)
        objectify.deannotate(
            dataItem, pytype=True, xsi=True, xsi_nil=False, cleanup_namespaces=False
        )
        etree.cleanup_namespaces(dataItem)

        if self.id:
            dataItem.set("id", self.id)
        if self.listElement:
            dataItem.set("listElement", self.listElement)
        if self.rootElement:
            dataItem.set("rootElement", self.rootElement)
        if self.schemaUri:
            dataItem.set("schemaUri", self.schemaUri)

        return dataItem

    def __str__(self) -> str:
        return f"DataItem: {self.id=} {self.name=}"
