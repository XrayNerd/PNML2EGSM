from PNML2EGSM.EGSM import (
    GuardedStageModel,
    DataFlowGuard,
    ProcessFlowGuard,
    Milestone,
    FaultLogger,
)
from lxml import objectify, etree


class Stage:
    parent: GuardedStageModel = None

    _tag = "stage"

    description: str | None
    id: str | None
    name: str | None
    task: str | None

    # Must have one or more
    dataFlowGuards: list
    milestones: list

    # Optional
    processFlowGuards: list
    subStages: list
    faultLoggers: list

    def __init__(
        self,
        description: str | None = None,
        id: str | None = None,
        name: str | None = None,
        task: str | None = None,
    ) -> None:
        self.description = description
        self.id = id
        self.name = name
        self.task = task

        self.dataFlowGuards = []
        self.processFlowGuards = []
        self.subStages = []
        self.milestones = []
        self.faultLoggers = []

    def setParent(self, parent: GuardedStageModel) -> None:
        self.parent = parent

    def addDataFlowGuard(self, dataFlowGuard: DataFlowGuard) -> None:
        self.dataFlowGuards.append(dataFlowGuard)
        dataFlowGuard.setParent(self)

    def addProcessFlowGuard(self, processFlowGuard: ProcessFlowGuard) -> None:
        self.processFlowGuards.append(processFlowGuard)
        processFlowGuard.setParent(self)

    def addFaultLogger(self, faultLogger: FaultLogger) -> None:
        self.faultLoggers.append(faultLogger)
        faultLogger.setParent(self)

    def addMilestone(self, milestone: Milestone) -> None:
        self.milestones.append(milestone)
        milestone.setParent(self)

    # Not Typed here due to Circular Import
    def addSubStage(self, subStage) -> None:
        self.subStages.append(subStage)
        subStage.setParent(self)

    def toElement(self):
        stage = objectify.Element(self._tag)
        objectify.deannotate(
            stage, pytype=True, xsi=True, xsi_nil=False, cleanup_namespaces=False
        )
        etree.cleanup_namespaces(stage)

        if self.id:
            stage.set("id", self.id)
        if self.name:
            stage.set("name", self.name)
        if self.description:
            stage.set("description", self.description)

        for dataFlowGuard in self.dataFlowGuards:
            stage.append(dataFlowGuard.toElement())

        for milestone in self.milestones:
            stage.append(milestone.toElement())

        for subStage in self.subStages:
            stage.append(subStage.toElement())

        for processFlowGuard in self.processFlowGuards:
            stage.append(processFlowGuard.toElement())

        for faultLogger in self.faultLoggers:
            stage.append(faultLogger.toElement())

        return stage


class SubStage(Stage):
    _tag = "subStage"
    parent: Stage

    def __init__(
        self,
        description: str | None = None,
        id: str | None = None,
        name: str | None = None,
        task: str | None = None,
    ) -> None:
        super().__init__(description, id, name, task)
