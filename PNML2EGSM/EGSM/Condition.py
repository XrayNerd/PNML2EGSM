from PNML2EGSM.EGSM import Milestone, Stage
from lxml import objectify, etree


class Condition:
    parent: Milestone
    _tag: str = "condition"

    description: str
    expression: str
    id: str
    language: str
    name: str

    def __init__(
        self,
        description: str | None = None,
        expression: str | None = None,
        id: str | None = None,
        language: str | None = None,
        name: str | None = None,
    ) -> None:
        self.description = description
        self.expression = expression
        self.id = id
        self.language = language
        self.name = name

    def setParent(self, parent: Stage) -> None:
        self.parent = parent

    def toElement(self):
        condition = objectify.Element(self._tag)
        objectify.deannotate(
            condition, pytype=True, xsi=True, xsi_nil=False, cleanup_namespaces=False
        )
        etree.cleanup_namespaces(condition)

        if self.expression:
            condition.set("expression", self.expression)
        if self.id:
            condition.set("id", self.id)
        if self.language:
            condition.set("language", self.language)
        if self.name:
            condition.set("name", self.name)
        if self.description:
            condition.set("description", self.description)

        return condition
