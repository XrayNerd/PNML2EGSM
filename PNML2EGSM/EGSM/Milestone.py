from PNML2EGSM.EGSM import Stage, Condition
from lxml import objectify, etree


class Milestone:
    parent: Stage
    _tag: str = "milestone"

    description: str | None
    eventIds: str
    id: str | None
    name: str | None

    condition: Condition = None

    def __init__(
        self,
        description: str | None = None,
        eventIds: str | None = None,
        id: str | None = None,
        name: str | None = None,
    ) -> None:
        self.description = description
        self.eventIds = eventIds
        self.id = id
        self.name = name

    def setParent(self, parent: Stage) -> None:
        self.parent = parent

    def setCondition(self, condition: Condition) -> None:
        self.condition = condition

    def toElement(self):
        milestone = objectify.Element(self._tag)
        objectify.deannotate(
            milestone, pytype=True, xsi=True, xsi_nil=False, cleanup_namespaces=False
        )
        etree.cleanup_namespaces(milestone)

        if self.eventIds:
            milestone.set("eventIds", self.eventIds)
        else:
            milestone.set("eventIds", "")
        if self.id:
            milestone.set("id", self.id)
        if self.name:
            milestone.set("name", self.name)
        if self.description:
            milestone.set("description", self.description)
        if self.condition:
            milestone.append(self.condition.toElement())

        return milestone

    def __str__(self) -> str:
        return f"{self.description=} {self.eventIds=} {self.id=} {self.name=}"
