
# PNML2EGSM

This tool is a result of a Master Thesis completed at the Technical University of Denmark, with the aim of providing a method of converting Petri Nets into E-GSM.

## Usage/Examples

```python
# Read in Petri Net and Workflow Tree files
petriNet, initial_marking, final_marking = pm4py.read_pnml("Location to PNML File")
wftree = parse_nodes("Location To WFTree Output")

# Convert to EGSM Object
out, infomodelxsd = Convert.convert_to_egsm(
    petriNet=petriNet,
    initial_marking=initial_marking,
    final_marking=final_marking,
    wftree=wftree,
)

# Save as XMI File
out_as_xmi = out.toElement()
etree.ElementTree(out_as_xmi).write(f"Temp XMI location")

# Convert into XML using XSL
dom = etree.parse("Temp XMI location")
xslt = etree.parse("PNML2EGSM/EGSM/utils/siena.xsl")
transform = etree.XSLT(xslt)
result = transform(dom)
result.write_output("Final EGSM Output")


```


## Acknowledgements

 - [BPMN2EGSM](https://bitbucket.org/polimiisgroup/bpmn2egsm/src/master/BPMN2GSM/)
 - [VIOLA](https://github.com/gemmadifederico/VIOLA)
## License

[CC-BY](https://creativecommons.org/licenses/by/4.0/)

