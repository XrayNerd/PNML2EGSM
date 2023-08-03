from PNML2EGSM.EGSM import (
    LifecycleModel,
    DataAccessModel,
    FlowModel,
    InformationModel,
    DocumentRoot,
    GuardedStageModel,
)
from lxml import objectify, etree


class Component:
    parent: DocumentRoot
    _namespace: str = "http://siena.ibm.com/model/CompositeApplication"
    _tag: str = "Component"

    accessControlModel: str | None
    id: str | None
    name: str | None
    lifecycleModel: LifecycleModel
    dataAccessModel: DataAccessModel
    flowModel: FlowModel
    informationModel: InformationModel
    guardedStageModel: GuardedStageModel

    def __init__(self, id: str | None = None, name: str | None = None) -> None:
        self.id = id
        self.name = name

        self.informationModel = None
        self.guardedStageModel = None

    def setParent(self, parent: DocumentRoot) -> None:
        self.parent = parent

    def setInformationModel(self, informationModel: InformationModel) -> None:
        self.informationModel = informationModel
        informationModel.setParent(self)

    def setGuardedStageModel(self, guardedStageModel: GuardedStageModel) -> None:
        self.guardedStageModel = guardedStageModel
        guardedStageModel.setParent(self)

    def toElement(self):
        tag = etree.QName(self._namespace, self._tag)
        component = objectify.Element(tag)
        objectify.deannotate(
            component, pytype=True, xsi=True, xsi_nil=False, cleanup_namespaces=False
        )
        etree.cleanup_namespaces(component)

        if self.id:
            component.set("id", self.id)
        if self.name:
            component.set("name", self.name)
        if self.informationModel:
            component.append(self.informationModel.toElement())
        if self.guardedStageModel:
            component.append(self.guardedStageModel.toElement())

        return component

    def __str__(self) -> str:
        return f"Component: {self.id=} {self.name=}"
