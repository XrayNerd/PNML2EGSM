from PNML2EGSM.EGSM import (
    LifecycleModel,
    DataAccessModel,
    FlowModel,
    DocumentRoot,
    DataItem,
    Component,
)
from lxml import objectify, etree


class InformationModel:
    parent: Component
    _tag = "informationModel"

    id: str | None
    rootDataItemId: str | None

    dataItem: DataItem

    def __init__(
        self, id: str | None = None, rootDataItemId: str | None = None
    ) -> None:
        self.id = id
        self.rootDataItemId = rootDataItemId
        self.dataItem = None

    def setParent(self, parent: Component) -> None:
        self.parent = parent

    def setDataItem(self, dataItem: DataItem):
        self.dataItem = dataItem
        dataItem.setParent(self)

    def toElement(self):
        informationModel = objectify.Element(self._tag)
        objectify.deannotate(
            informationModel,
            pytype=True,
            xsi=True,
            xsi_nil=False,
            cleanup_namespaces=False,
        )
        etree.cleanup_namespaces(informationModel)

        if self.id:
            informationModel.set("id", self.id)
        if self.rootDataItemId:
            informationModel.set("rootDataItemId", self.rootDataItemId)
        if self.dataItem:
            informationModel.append(self.dataItem.toElement())

        return informationModel

    def __str__(self) -> str:
        return f"Information Model: {self.id=} {self.name=}"
