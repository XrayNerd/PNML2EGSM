from typing import Optional, Union
from pm4py import PetriNet
from processmining.PNML2EGSM.EGSM import (
    SubStage,
    Stage,
    DataFlowGuard,
    ProcessFlowGuard,
    Milestone,
    FaultLogger,
    GuardedStageModel,
    DocumentRoot,
    Component,
    InformationModel,
    DataItem,
    EventModel,
    Event,
    Condition,
)

import xml.etree.ElementTree as ET

from itertools import permutations, pairwise

from pm4py.objects.petri_net.utils.initial_marking import discover_initial_marking
from pm4py.objects.petri_net.utils.petri_utils import pre_set, post_set

from processmining.PNML2EGSM.wftree import (
    Fragment,
    RPSTType,
    get_fragment_depth,
    parse_nodes,
    WFTreeRefinedType,
)


def convert_to_egsm(petriNet: PetriNet, initial_marking, final_marking, wftree):
    docRoot = DocumentRoot(kwargs={"name": "Definitions_1_application"})
    component = Component(id="Definitions_1")
    eventModel = EventModel(
        id="Definitions_1_eventModel", name="Definitions_1_eventModel"
    )
    informationModel = InformationModel(id="infoModel", rootDataItemId="infoModel")
    dataItem = DataItem(
        id="infoModel", rootElement="infoModel", schemaUri="data/infoModel.xsd"
    )

    infomodelxsd = ET.Element(
        "xs:schema",
        {
            "xmlns:xs": "http://www.w3.org/2001/XMLSchema",
            "attributeFormDefault": "unqualified",
            "elementFormDefault": "qualified",
        },
    )

    docRoot.addComponent(component=component)
    docRoot.addEventModel(eventModel=eventModel)
    component.setInformationModel(informationModel=informationModel)
    informationModel.setDataItem(dataItem=dataItem)

    guardedStageModel = GuardedStageModel(id="Definitions_1")

    init_marking = discover_initial_marking(petri=petriNet)
    places: dict[str, PetriNet.Place] = {}
    transitions: dict[str, PetriNet.Transition] = {}
    entries: dict[str, list[Fragment]] = {}
    exits: dict[str, list[Fragment]] = {}
    for place in petriNet.places:
        place_name_tag = place.properties["place_name_tag"]
        entries[place_name_tag] = []
        exits[place_name_tag] = []
        places[place_name_tag] = place

    for transition in petriNet.transitions:
        if not transition.label:
            continue
        entries[transition.label] = []
        exits[transition.label] = []
        transitions[transition.label] = transition

    fragments: dict[str, Fragment] = wftree[0]
    root: Optional[Fragment] = wftree[1]
    starting_place: Optional[PetriNet.Place]
    if not initial_marking and root:
        initial_marking = places[root.entry]
    for id_, fragment in fragments.items():
        if fragment.entry in entries.keys():
            entries[fragment.entry].append(fragment)
        else:
            entries[fragment.entry] = []
            entries[fragment.entry].append(fragment)
        if fragment.exit_ in exits.keys():
            exits[fragment.exit_].append(fragment)
        else:
            exits[fragment.exit_] = []
            exits[fragment.exit_].append(fragment)

    def get_next_places(in_marking) -> list[PetriNet.Place]:
        next_marking = post_set(in_marking)
        out_places = []
        otherwise = []
        for item in next_marking:
            if isinstance(item, PetriNet.Place):
                out_places.append(item)
            else:
                otherwise.append(item)
        if len(out_places) == 0:
            for item in otherwise:
                out_places += get_next_places(item)
        return out_places

    def get_next_transitions(in_marking) -> list[PetriNet.Transition]:
        next_marking = post_set(in_marking)
        out_transitions = []
        otherwise = []
        for item in next_marking:
            if isinstance(item, PetriNet.Transition):
                # Ignore if Tau
                if item.label:
                    out_transitions.append(item)
                else:
                    otherwise.append(item)
            else:
                otherwise.append(item)
        if len(out_transitions) == 0:
            for item in otherwise:
                out_transitions += get_next_transitions(item)
        return out_transitions

    def get_prev_places(in_marking) -> list[PetriNet.Place]:
        prev_marking = pre_set(in_marking)
        out_places = []
        otherwise = []
        for item in prev_marking:
            if isinstance(item, PetriNet.Place):
                out_places.append(item)
            else:
                otherwise.append(item)
        if len(out_places) == 0:
            for item in otherwise:
                out_places += get_prev_places(item)
        return out_places

    def get_prev_transitions(
        in_marking, check_for_tau=False
    ) -> list[PetriNet.Transition]:
        prev_marking = pre_set(in_marking)
        out_transitions = []
        otherwise = []
        for item in prev_marking:
            if isinstance(item, PetriNet.Transition):
                # Ignore if Tau
                if item.label or check_for_tau:
                    out_transitions.append(item)
                else:
                    otherwise.append(item)
            else:
                otherwise.append(item)
        if len(out_transitions) == 0:
            for item in otherwise:
                out_transitions += get_prev_transitions(item)
        return out_transitions

    def search_branches(in_marking) -> list[Fragment]:
        branches = []
        for key, fragment in fragments.items():
            nodes = set([t for x in fragment.nodes for t in x])
            if in_marking.name in nodes:
                branches.append(fragment)
        return branches

    def get_branches_by_entries(in_marking) -> list[Fragment]:
        name_tag = None
        branches = []
        if isinstance(in_marking, PetriNet.Place):
            name_tag = "place_name_tag"
        else:
            name_tag = "trans_name_tag"
        for fragment in entries[in_marking.properties[name_tag]]:
            if fragment.type_ == RPSTType.TRIVIAL:
                branches.append(fragment._parent)
                continue
            branches.append(fragment)
        return branches

    def get_branches_by_exits(in_marking) -> list[Fragment]:
        name_tag = None
        branches = []
        if isinstance(in_marking, PetriNet.Place):
            name_tag = "place_name_tag"
        else:
            name_tag = "trans_name_tag"
        for fragment in exits[in_marking.properties[name_tag]]:
            if fragment.type_ == RPSTType.TRIVIAL:
                branches.append(fragment._parent)
                continue
            branches.append(fragment)
        return branches

    def get_highest_branch(in_marking, by_entry=True) -> Optional[Fragment]:
        highest_branch = (None, 1000000000)
        if by_entry:
            for branch in get_branches_by_entries(in_marking):
                fragment_depth = get_fragment_depth(branch)
                if fragment_depth < highest_branch[1]:
                    highest_branch = (branch, fragment_depth)
        else:
            for branch in get_branches_by_exits(in_marking):
                fragment_depth = get_fragment_depth(branch)
                if fragment_depth < highest_branch[1]:
                    highest_branch = (branch, fragment_depth)
        return highest_branch[0]

    def get_above_parallel_branch(fragment: Fragment, depth=0) -> Optional[Fragment]:
        if isinstance(fragment, Fragment):
            if depth > 0:
                if fragment.refinedType == WFTreeRefinedType.TRANSITION_BORDERED:
                    return fragment
            if isinstance(fragment._parent, Fragment):
                return get_above_parallel_branch(
                    fragment=fragment._parent, depth=depth + 1
                )
            else:
                return None
        else:
            return None

    def get_immediate_prev_tau_transitions(in_marking):
        prev = pre_set(in_marking)
        tau_trans = []
        for item in prev:
            item_prev = pre_set(item)
            for trans in item_prev:
                if not trans.label:
                    tau_trans.append(trans)
        return tau_trans

    def is_tau_route_to_start(in_marking):
        tau = get_immediate_prev_tau_transitions(in_marking)
        path = False
        while len(tau) > 0:
            curr_tau = tau.pop()
            for item in pre_set(curr_tau):
                if item.properties["place_name_tag"] == "source":
                    path = True
                    break
            tau.extend(get_immediate_prev_tau_transitions(curr_tau))
        return path

    component.setGuardedStageModel(guardedStageModel=guardedStageModel)
    milestone_deps = []
    milestones = {}
    for label, transition in transitions.items():
        name_tag = "trans_name_tag"
        name = transition.properties[name_tag]

        # Create an event
        event_name = f"{name}"

        event = Event(id=event_name, name=event_name)
        eventModel.addEvent(event=event)

        # Create event for information Model: Credit: Viola: https://github.com/gemmadifederico/VIOLA/blob/master/DFG2EGSM/build-xml.py#L64C12-L64C12
        elem = ET.SubElement(infomodelxsd, "xs:element", {"name": event_name})
        ct = ET.SubElement(elem, "xs:complexType")
        attr = ET.SubElement(
            ct,
            "xs:attribute",
            {"name": "timestamp", "type": "xs:dateTime", "use": "required"},
        )

        # S containing sub_stage S_run, check T's conformity
        stage = Stage(id=name, name=name)
        # S_run for the running of Transition T
        stage_run = SubStage(id=f"{name}_run", name=f"{name}_run")

        stage.addSubStage(subStage=stage_run)
        guardedStageModel.addStage(stage=stage)

        # Data Flow Guard on expected transition T
        dfg_s = DataFlowGuard(
            id=f"{name}_dfg",
            name=f"{name} Data Flow Guard",
            expression=f"GSM.isEventOccurring({event_name})",
            eventIds=event_name,
            language="JEXL",
        )
        stage.addDataFlowGuard(dataFlowGuard=dfg_s)

        # Data Flow Guard on sub-stage
        dfg_s_run = DataFlowGuard(
            id=f"{name}_run_dfg",
            name=f"{name}_run Data Flow Guard",
            expression=f"GSM.isEventOccurring({event_name})",
            eventIds=event_name,
            language="JEXL",
        )

        stage_run.addDataFlowGuard(dataFlowGuard=dfg_s_run)

        milestone_s = Milestone(id=f"{name}_m")
        stage.addMilestone(milestone=milestone_s)

        next_trans = get_next_transitions(transition)
        # Non Parallel Branching Milestone
        if len(next_trans) == 1:
            evnt = f"{next_trans[0].properties[name_tag]}"
            milestone_s.eventIds = evnt
            condition = Condition(
                expression=f"GSM.isEventOccurring({evnt})",
                id=f"{name}_m_c",
                name=f"{name} Milestone Condition",
                language="JEXL",
            )
            milestone_s.setCondition(condition=condition)
        # It is the final transition
        elif len(next_trans) == 0:
            condition = Condition(
                expression=f"GSM.isMilestoneAchieved({name}_run)",
                id=f"{name}_m_c",
                name=f"{name} Milestone Condition",
                language="JEXL",
            )
            milestone_s.setCondition(condition=condition)
        # Branching Milestone
        else:
            highest_branch: Optional[Fragment] = get_highest_branch(transition)
            milestones[transition.properties[name_tag]] = (
                milestone_s,
                transition,
                highest_branch,
            )
            # Parallel Branching Milestone
            if highest_branch:
                if highest_branch.refinedType == WFTreeRefinedType.TRANSITION_BORDERED:
                    above_parallel_branch = get_above_parallel_branch(highest_branch)
                    if above_parallel_branch:
                        milestone_deps.append(
                            (
                                above_parallel_branch.entry,
                                transition.properties[name_tag],
                            )
                        )
                else:
                    expressions = []
                    if transition in next_trans:
                        next_trans.remove(transition)
                        expressions.append(f"GSM.isMilestoneAchieved({name}_run)")

                    expr = [
                        f"GSM.isStageActive({x.properties[name_tag]})"
                        for x in next_trans
                    ]
                    expr = " or ".join(expr)
                    expressions.append(expr)
                    expr = " or ".join(expressions)
                    condition = Condition(
                        expression=expr,
                        id=f"{name}_m_c",
                        name=f"{name} Milestone Condition",
                        language="JEXL",
                    )
                    milestone_s.setCondition(condition=condition)

        # Milestone for Sub Stage T_run
        milestone_s_run = Milestone(
            id=f"{name}_run_m",
            eventIds=event_name,
        )
        condition_run = Condition(
            expression=f"GSM.isEventOccurring({event_name})",
            id=f"{name}_m_c",
            name=f"{name} Milestone Condition",
            language="JEXL",
        )
        milestone_s_run.setCondition(condition_run)
        stage_run.addMilestone(milestone=milestone_s_run)

        # PFG
        prev_trans = get_prev_transitions(transition)
        # self_loop = False
        # if transition in prev_trans:
        #     self_loop = True
        #     prev_trans.remove(transition)
        pfg = None
        skip = False
        if len(prev_trans) == 1:
            expressions = []
            expr = ""
            if transition in prev_trans:
                expressions.append(f"GSM.isMilestoneAchieved({name}_run)")
                prev_trans.remove(transition)
            # Check for Tau
            if len(prev_trans) == 0:
                starts = []
                for fragment in search_branches(transition):
                    if fragment.entry in transitions:
                        starts.append(fragment.entry)
                if len(starts) == 0:
                    # The Transition is proceeded by no other transitions
                    skip = True
                    temp = [x for x in transitions.keys()]
                    temp.remove(name)
                    expr = [f"GSM.isStageActive({t})" for t in temp]
                    expr = " and ".join(expr)
                    expr = f"not ({expr})"
                    if len(expressions) > 0:
                        expr = f"({expr})"
                    expressions.append(expr)
                expr = " or ".join(expressions)
            else:
                expr = f"GSM.isStageActive({prev_trans[0].properties[name_tag]})"
            pfg_s = ProcessFlowGuard(
                id=f"{name}_pfg", name=f"{name} Process Flow Guard", expression=expr
            )
            stage.addProcessFlowGuard(pfg_s)
        elif len(prev_trans) == 0:
            # The non activity of all other stages...
            skip = True
            temp = [x for x in transitions.keys()]
            temp.remove(name)
            expr = [f"GSM.isStageActive({t})" for t in temp]
            expr = " and ".join(expr)
            expr = f"not ({expr})"
            pfg_s = ProcessFlowGuard(
                id=f"{name}_pfg", name=f"{name} Process Flow Guard", expression=expr
            )
            stage.addProcessFlowGuard(pfg_s)
        else:
            # Merges
            # Parallel branch merge
            prev_places = get_prev_places(transition)
            if len(prev_places) > 1:
                prev_trans = []
                for place in prev_places:
                    trans = get_prev_transitions(place)
                    prev_trans.append(trans)
                expressions = []
                for group in prev_trans:
                    group_labels = [x.properties[name_tag] for x in group]
                    expr = [f"GSM.isStageActive({x})" for x in group_labels]
                    expr = " or ".join(expr)
                    if len(group_labels) > 1:
                        expr = f"({expr})"
                    expressions.append(expr)
                expressions = " and ".join(expressions)

                pfg_s = ProcessFlowGuard(
                    id=f"{name}_pfg",
                    name=f"{name} Process Flow Guard",
                    expression=expressions,
                )
                stage.addProcessFlowGuard(pfg_s)
            else:
                expr = []
                # Exclusive branch merge

                # Deal with Self Loops
                if transition in prev_trans:
                    expr.append(f"GSM.isMilestoneAchieved({name}_run)")
                    prev_trans.remove(transition)
                labels = [x.properties[name_tag] for x in prev_trans]
                expr.extend([f"GSM.isStageActive({x})" for x in labels])
                expr = " or ".join(expr)
                pfg_s = ProcessFlowGuard(
                    id=f"{name}_pfg", name=f"{name} Process Flow Guard", expression=expr
                )
                stage.addProcessFlowGuard(pfg_s)
        if is_tau_route_to_start(transition) and not skip:
            temp = [x for x in transitions.keys()]
            temp.remove(name)
            expr = [f"GSM.isStageActive({t})" for t in temp]
            expr = " and ".join(expr)
            expr = f"not ({expr})"
            stage.processFlowGuards[
                0
            ].expression = f"{stage.processFlowGuards[0].expression} or ({expr})"

    # Joins linked tuples together into a sorted list
    def connect_tuples(in_list):
        iter_list = in_list
        updated = False
        while not updated:
            updated = True
            for a, b in permutations(iter_list, r=2):
                if b[0] == a[-1]:
                    iter_list.remove(a)
                    iter_list.remove(b)
                    iter_list.append((*a, b[-1]))
                    updated = False
                    break
        return iter_list

    # Deal with Milestones that are in parallel branches
    for link in connect_tuples(in_list=milestone_deps):
        used = {}
        for label in reversed(list(link)):
            milestone, trans, branch = milestones[label]
            sub_branches = []
            expressions = []
            for sub_branch in branch.children:
                branch_expression = ""
                extended_expression = ""
                sub_trans = [x for t in sub_branch.nodes for x in t]
                sub_trans = set(sub_trans).intersection(set(transitions.keys()))
                sub_trans.remove(sub_branch.entry)
                sub_trans.remove(sub_branch.exit_)
                sub_trans = tuple(sub_trans)
                all_trans = sub_trans
                for key, expression in used.items():
                    x = set([x for t in key for x in t])
                    y = set([x for t in sub_trans for x in t])
                    if x.intersection(y):
                        sub_trans = tuple(y - x)
                        extended_expression = expression
                expr = " or "
                branch_expression = [
                    f"GSM.isMilestoneAchieved({t})" for t in list(sub_trans)
                ]
                expr = f"{expr.join(branch_expression)}"
                if extended_expression:
                    expr = f"{expr} or {extended_expression}"
                if len(all_trans) > 1:
                    expr = f"({expr})"
                expressions.append(expr)
                sub_branches.append(all_trans)
            expr = " and "
            expr = expr.join(expressions)
            expr = f"({expr})"
            used[tuple(x for t in sub_branches for x in t)] = expr

            name_tag = "trans_name_tag"
            name = trans.properties[name_tag]
            condition = Condition(
                expression=f"{expr}",
                id=f"{name}_m_c",
                name=f"{name} Milestone Condition",
                language="JEXL",
            )
            milestone.setCondition(condition=condition)

    return docRoot, infomodelxsd
