"""
XML parse test:
Floris M

"""
import xml.etree.ElementTree as ET # for parsing the output .xml files from MEME and Fimo.

from pathlib import Path # to use the working dir variable.
WORKING_DIR = Path.cwd()


def xml_parser():
    motif_dict = {}
    tree = ET.parse(WORKING_DIR / "User_output/meme/meme.xml")
    root = tree.getroot()
    meme_version = (root.attrib["version"]) # meme version used.
    for motifs in root.findall("motifs"):
        for motif in motifs:
            print(f"{motif.attrib["id"]} with a P-value of {motif.attrib["p_value"]} motif width: {motif.attrib["width"]}") # print-f with same information as the motif_dict.
            motif_dict[motif.attrib["id"]] = (motif.attrib["p_value"], motif.attrib["width"], motif.attrib["sites"]) # Dict with as key the motif id (number) and p-value as value.
        
    for i in motif_dict: # demo how to get the data from the dict
        # motif_dict: first position: motif number. second position: motif width. third position: sites
        print(f"motif number and width: {motif_dict[i]}")


    # print(motif_dict)

xml_parser()


