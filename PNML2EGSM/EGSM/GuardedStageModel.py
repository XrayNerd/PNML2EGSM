from PNML2EGSM.EGSM import Stage, Component
from lxml import objectify, etree


class GuardedStageModel:
    parent: Component
    _tag = "guardedStageModel"

    description: str | None
    id: str | None
    name: str | None

    stages = []
    component: Component = None

    def __init__(
        self,
        description: str | None = None,
        id: str | None = None,
        name: str | None = None,
    ) -> None:
        self.description = description
        self.id = id
        self.name = name

    def setParent(self, parent: Component) -> None:
        self.parent = parent

    def addStage(self, stage: Stage) -> None:
        self.stages.append(stage)
        stage.setParent(self)

    def toElement(self):
        guardedStageModel = objectify.Element(self._tag)
        objectify.deannotate(
            guardedStageModel,
            pytype=True,
            xsi=True,
            xsi_nil=False,
            cleanup_namespaces=False,
        )
        etree.cleanup_namespaces(guardedStageModel)

        if self.id:
            guardedStageModel.set("id", self.id)
        if self.name:
            guardedStageModel.set("name", self.name)
        if self.description:
            guardedStageModel.set("description", self.description)

        for stage in self.stages:
            guardedStageModel.append(stage.toElement())

        return guardedStageModel
