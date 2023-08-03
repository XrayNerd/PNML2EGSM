from lxml import etree

from processmining.PNML2EGSM.EGSM import (
    GuardedStageModel,
    Stage,
    DataFlowGuard,
    ProcessFlowGuard,
    SubStage,
    Milestone,
    Condition,
    FaultLogger,
    Component,
    Event,
    EventModel,
    DocumentRoot,
    InformationModel,
    DataItem,
)


class Parser:
    def parse(self, file: str):
        tree = etree.parse(file)
        root = tree.getroot()

        documentRoot = DocumentRoot(**root.attrib)

        # Create the ComponentType Objects
        componentType = root[0]
        component = Component(**componentType.attrib)
        documentRoot.addComponent(component=component)

        # Create the Event Model Objects
        eventModelType = root[1]
        eventModel = EventModel(**eventModelType.attrib)
        documentRoot.addEventModel(eventModel)
        # Add all Events attached to the Event Model
        for element in eventModelType.iter():
            match element.tag:
                case "event":
                    event = Event(**element.attrib)
                    eventModel.addEvent(event=event)
                case _:
                    # TODO: Log unmatching event tags.
                    pass

        # Create the Information Model Object
        informationModelType = componentType[0]
        informationModel = InformationModel(**informationModelType.attrib)
        component.setInformationModel(informationModel=informationModel)
        # Add Sub Elements under Information Model
        for element in informationModelType.iter():
            match element.tag:
                case "dataItem":
                    dataItem = DataItem(**element.attrib)
                    informationModel.setDataItem(dataItem=dataItem)
                case _:
                    # TODO: Log Unmatched Information Model Sub Types...
                    pass

        # Create the Guarded Stage Model object
        guardedStageModelType = componentType[1]
        guardedStageModel = GuardedStageModel(**guardedStageModelType.attrib)
        component.setGuardedStageModel(guardedStageModel=guardedStageModel)

        # Create and match Stage, DFG, PFG, Milestone, Fault Logger, and other subtype objects
        stages = {}
        milestones = {}
        for element in guardedStageModelType.iter():
            match element.tag:
                case "stage":
                    stage = Stage(**element.attrib)
                    stages[stage.id] = stage
                    guardedStageModel.addStage(stage=stage)
                case "subStage":
                    subStage = SubStage(**element.attrib)
                    stages[subStage.id] = subStage
                    stages[element.getparent().get("id")].addSubStage(subStage=subStage)
                case "dataFlowGuard":
                    dfg = DataFlowGuard(**element.attrib)
                    stages[element.getparent().get("id")].addDataFlowGuard(
                        dataFlowGuard=dfg
                    )
                case "milestone":
                    milestone = Milestone(**element.attrib)
                    milestones[milestone.id] = milestone
                    stages[element.getparent().get("id")].addMilestone(
                        milestone=milestone
                    )
                case "condition":
                    condition = Condition(**element.attrib)
                    milestones[element.getparent().get("id")].setCondition(
                        condition=condition
                    )
                case "processFlowGuard":
                    pfg = ProcessFlowGuard(**element.attrib)
                    stages[element.getparent().get("id")].addProcessFlowGuard(
                        processFlowGuard=pfg
                    )
                case "faultLogger":
                    faultLogger = FaultLogger(**element.attrib)
                    stages[element.getparent().get("id")].addFaultLogger(
                        faultLogger=faultLogger
                    )
                case _:
                    # TODO: Log here that we got something not currently registered...
                    pass

        return documentRoot
