from typing import Optional
from PNML2EGSM.EGSM.utils import Convert
from PNML2EGSM.wftree import (
    Fragment,
    parse_nodes,
)
import pm4py
from lxml import etree
import xml.etree.ElementTree as ET
from sklearn.model_selection import train_test_split

def create_test_train(input_logs: str):
    log = pm4py.read_xes(input_logs)
    df = pm4py.convert_to_dataframe(log)

    train, test = train_test_split(df, test_size=0.2)
    name = input_logs.split("/")[-1].split(".")[0]
    train_file = f"{OUTPUT_FOLDER}{name}_training.xes.gz"
    test_file = f"{OUTPUT_FOLDER}{name}_testing.xes.gz"

    pm4py.write_xes(train, train_file, case_id_key="case:concept:name")
    pm4py.write_xes(test, test_file, case_id_key="case:concept:name")

    return (train_file, test_file)


def produce_graphs(data: str):
    log = pm4py.read_xes(data)

    file = "anonymised_data"

    dfg, start_activities, end_activities = pm4py.discover_dfg(log)
    pm4py.write_dfg(
        dfg=dfg,
        start_activities=start_activities,
        end_activities=end_activities,
        file_path=f"{OUTPUT_FOLDER}{file}_dfg.dfg",
    )
    pm4py.save_vis_dfg(
        dfg=dfg,
        start_activities=start_activities,
        end_activities=end_activities,
        file_path=f"{OUTPUT_FOLDER}{file}_dfg.png",
    )

    process_model, inital_marking, final_marking = pm4py.discover_petri_net_inductive(
        log, multi_processing=True
    )
    pm4py.write_pnml(
        petri_net=process_model,
        initial_marking=inital_marking,
        final_marking=final_marking,
        file_path=f"{OUTPUT_FOLDER}{file}_inductive.pnml",
    )
    pm4py.save_vis_petri_net(
        process_model,
        inital_marking,
        final_marking,
        f"{OUTPUT_FOLDER}{file}_petri_inductive.png",
    )

    # TODO: ADJUSTMENTS
    # Add ID to Definitions tag
    # Change xmlns:bpmn to xlmns:bpmn2
    # Change "bpmn:" to "bpmn2:"
    # Change "converging" to "Converging"
    # Change "diverging" to "Diverging"
    bpmn_graph = pm4py.discover_bpmn_inductive(log, multi_processing=True)
    pm4py.write_bpmn(
        model=bpmn_graph, file_path=f"{OUTPUT_FOLDER}{file}_inductive.bpmn"
    )
    pm4py.save_vis_bpmn(
        bpmn_graph=bpmn_graph, file_path=f"{OUTPUT_FOLDER}{file}_bpmn_inductive.png"
    )


def convert_pnml2egsm():
    petriNet, initial_marking, final_marking = pm4py.read_pnml(
        f"{OUTPUT_FOLDER}anonymised_data_inductive.pnml", auto_guess_final_marking=True
    )
    wftree: tuple[dict[str, Fragment], Optional[Fragment]] = parse_nodes(
        f"{OUTPUT_FOLDER}anonymised_data.wftree"
    )

    out, infomodelxsd = Convert.convert_to_egsm(
        petriNet=petriNet,
        initial_marking=initial_marking,
        final_marking=final_marking,
        wftree=wftree,
    )

    out_element = out.toElement()
    etree.ElementTree(out_element).write(
        f"{OUTPUT_FOLDER}petri_net_egsm.xmi",
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8",
    )

    dom = etree.parse(f"{OUTPUT_FOLDER}petri_net_egsm.xmi")
    xslt = etree.parse(
        "PNML2EGSM/EGSM/utils/siena.xsl"
    )
    transform = etree.XSLT(xslt)
    result = transform(dom)
    result.write_output(f"{OUTPUT_FOLDER}petri_net_dervied_egsm.xml")

    # Credit to VIOLA: https://github.com/gemmadifederico/VIOLA/blob/master/DFG2EGSM/build-xml.py#L45
    ET.ElementTree(infomodelxsd).write(
        f"{OUTPUT_FOLDER}petri_net_derived_infoModel.xsd",
        xml_declaration=True,
        encoding="utf-8",
    )

if __name__ == "__main__":
    # input_logs = "Location of Event Logs"

    # train_file, test_file = create_test_train(input_logs=input_logs)
    # OR
    # train_file = "Location for Training Data"
    # test_file = "Location for Testing Data"

    # produce_graphs(data=train_file)

    # convert_pnml2egsm()
    pass