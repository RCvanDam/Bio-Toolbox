
"""
MemeSuite backend for website
Author: Tai Vo, Floris M, Jarno Duiker, Ruben van Dam
Date: 7-03-2024
Last updated: 08-04-2024

Version: 0.16

"""

import subprocess # To execute terminal command's on the computer.
import os
import tarfile
from pathlib import Path # to use the working dir variable.
import shutil # to move around output files.
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET # for parsing the output .xml files from MEME and Fimo.


# Global test variables (should be replaced by the ones given back by the webserver.)
# WORKING_DIR = os.path.dirname(os.path.realpath(__file__)) # to check current dir

WORKING_DIR = Path.cwd()
if "/app_prototype" not in str(WORKING_DIR): # If the working dir is in the root of the project.
    WORKING_DIR = WORKING_DIR / "app_prototype/"

print(WORKING_DIR)


# Test variables for FIMO
database_to_use = False # Name of the database.
use_default_p_value = True # True or false
p_value = 0.0001 # float, default is 0.0001.
input_motif_file = "{}/Motif_databases/SwissRegulon_e_coli.meme".format(WORKING_DIR)
input_sequence_path_fimo = "{}/meme_sample_sequences.fasta".format(WORKING_DIR) # replace with relative path.
output_path_fimo = "{}/User_output/fimo".format(WORKING_DIR) # (Temporary) storage place for the generated files.


# Test variables for MEME
max_amount_of_motifs = 20 # max abount of motif to look for, program stops looking if the number is exceeded.
max_motif_size = 8 # max length of the motifs.
min_motif_size = 3
alphabet = "dna" # Nucleotide alphabet to use: RNA, DNA or protein.
input_sequence_path_meme = "{}/meme_sample_sequences.fasta".format(WORKING_DIR)
output_path_meme = "{}/User_output/meme".format(WORKING_DIR)
home_path = subprocess.run("echo $HOME", shell=True, text=True, capture_output=True).stdout.rstrip()


class Fimo:
    """
    The Fimo class serves the purpose of running the Fimo tool after the parameters from the website are collected.

    :param database_to_use: The motif file to use when the user doesn't provide their own.
    :param use_default_p_value: True or False, whether or not to use the default P-value.
    :param p_value: If chosen, the custom P-value.
    """

    def __init__(self, database_to_use, use_default_p_value, p_value, input_motif_file, input_sequence_path_fimo, output_path_fimo):
        """
        Init function to initialize the class with the parameters above. 
        """
        self.database_to_use = database_to_use
        self.use_default_p_value = use_default_p_value
        self.p_value = p_value
        self.input_motif_file = input_motif_file
        self.input_sequence_path_fimo = input_sequence_path_fimo
        self.output_path_fimo = output_path_fimo
        self.motif_dict = ""
        # self.is_multifasta()

    def __str__(self):
        """
        Returns information about the created object.
        """
        return f"Database used: {database_to_use}, Default p-value used?: {use_default_p_value}, P-value: {p_value}"

    def is_id(line):
        return line[0] == ">"

    def is_multifasta(fastafile):
        """
        Detects whether a file is fasta or multifasta
        :param str fastafile: the filepath of the fastafile you want to check
        """
        with open(fastafile, "r") as fasta:
            return len(list(filter(is_id,fasta))) >= 2


    def run(self):
        """
        Using the ".run()" method, the Fimo tool will be run. No parameters needed because they were already given when the class was initialized.
        """

        # input_motif_file = WORKING_DIR + "/Motif_databases/SwissRegulon_human_and_mouse.meme"

        if database_to_use: # If the user selected one of the databases instead of a motif file.
            if database_to_use == "Human":
                input_motif_file = WORKING_DIR + "/Motif_databases/HOCOMOCOv11_full_HUMAN_mono_meme_format.meme"

            elif database_to_use == "Mouse":
                input_motif_file = WORKING_DIR + "/Motif_databases/HOCOMOCOv11_full_MOUSE_mono_meme_format.meme"

            elif database_to_use == "Drosophilla (fly)":
                input_motif_file = WORKING_DIR + "/Motif_databases/OnTheFly_2014_Drosophila.meme"

            elif database_to_use == "E.coli (Bacterium)":
                input_motif_file = WORKING_DIR + "/Motif_databases/SwissRegulon_e_coli.meme"

            elif database_to_use == "Jaspar":
                input_motif_file = WORKING_DIR + "/Motif_databases/SwissRegulon_human_and_mouse.meme"
            
            # Run the tool with the selected database:

            # Uncomment to directly activate the tool here...
            # fimo_command = "fimo --oc {} --verbosity 2 --bgfile --nrdb-- --thresh 0.001 {} {}".format(output_path_fimo, input_motif_file, input_sequence_path_fimo)
            # fimo_output = subprocess.run([fimo_command], executable="/bin/sh", shell=True, text=True)
            # output_fimo = fimo_output.stdout
            # print(output_fimo)
            # return

        else: # if not: use a given motif file.
            fimo_command = "fimo --oc {} --verbosity 2 --bgfile --nrdb-- --thresh 0.001 {} {}".format(output_path_fimo, self.input_motif_file, self.input_sequence_path_fimo)

        if use_default_p_value == True: # if the user chooses the default P-value:
            p_value = 0.0001 # The default p_value
            # fimo_command = "fimo --oc WORKING_DIR +/User_output/meme --verbosity 2 --bgfile --nrdb-- --thresh {} {} {}".format(p_value, input_motif_file, self.input_sequence_path_fimo)
            fimo_command = "fimo --oc {} --verbosity 2 --bgfile --nrdb-- --thresh {} {} {}".format(output_path_fimo, p_value, input_motif_file, input_sequence_path_fimo)


        fimo_output = subprocess.run([fimo_command], executable="/bin/sh", shell=True, text=True)
        output_fimo = fimo_output.stdout
        print(output_fimo) # should be redirected to the ouput display in the website.


class Meme:
    """
    Meme class to use user input with the meme-tool.
    :param: # to-do fill in params
    """

    def __init__(self, max_amount_of_motifs, max_motif_size, min_motif_size, alphabet, input_sequence_path_meme, output_path_meme):
        """
        Init function to initialize the class with the parameters above. 
        """
        self.max_amount_of_motifs = max_amount_of_motifs
        self.max_motif_size = max_motif_size
        self.min_motif_size = min_motif_size
        self.alphabet = alphabet
        self.input_sequence_path_meme = input_sequence_path_meme
        self.output_path_meme = output_path_meme
        self.new_env = None

    def __str__(self):
        """
        Return string with information about the used parameters that were used to initialize the class. 
        """
        return f"Max amount of motifs: {self.max_amount_of_motifs}, Max motif size: {self.max_motif_size}, Min motif size: {self.min_motif_size}, Alphabet used: {self.alphabet}."

    def add_to_path(self):
        """
        If memeSuite is not added to the PATH, this method can add it.

        """
        print("in Path?")
        meme_in_path = subprocess.run("echo $PATH", shell=True, text=True, capture_output=True).stdout
        print(f"Path: {meme_in_path}")
        if "meme" in meme_in_path:
            print("Memsuite in path")
        else:
            print("memesuite not in path, adding now...")
            self.new_env = os.environ.copy()
            self.new_env["PATH"] = os.pathsep.join([f"{home_path}/bin/meme:$PATH", self.new_env["PATH"]])

            meme_in_path = subprocess.run("echo $PATH", shell=True, text=True, capture_output=True, env=self.new_env).stdout
            print(f"Path: {meme_in_path}")

    def run(self): # add commandline execution using the user given parameters.
        #print(f"Het gebruitke alphabet is:: .self: {self.alphabet} en {alphabet}")
        print(f"Alphabet: {self.alphabet}")
        if is_multifasta(input_sequence_path_meme):
            # meme_command_test = "meme '/home/floris/Documenten/Data_semax_amount_of_motifst/DATA/meme_sample_sequences' -dna -oc ~/Documenten/OUTPUT_DATA/MEME/ -time 14400 -mod zoops -nmotifs 3 -minw 6 -maxw 50 -objfun classic -revcomp -markov_order 0"
            meme_command_test = "meme {} -{} -oc {} -time 14400 -mod zoops -nmotifs {} -minw 6 -maxw 50 -objfun classic -revcomp -markov_order 0".format(
            self.input_sequence_path_meme, self.alphabet, self.output_path_meme, self.max_amount_of_motifs)
            # print(f"Running command: {meme_command_test}\nwith PATH: {self.new_env['PATH']}\n")godverdomme ruben
            
            meme_output = subprocess.run([meme_command_test],  executable="/bin/sh", shell=True, text=True, env=self.new_env)
            output_meme = meme_output.stdout
            print(output_meme) # should be redirected to the ouput display in the website.
            self.generate_tarfile()
            html_output_file_mover()
            memelogo_mover()
            self.motif_dict = xml_parser()
        else:
            print("To use the MEME command, please use a multi-fasta file as input")

    def weblogo_checker(self):
        """"
        in this function i want to check the weblogo
        and display the one that has the best accuracy
        :param: all generated weblogo
        :return: best weblogo
        """
        
        weblogo_jpg_list = []
        for files in os.listdir(output_path_meme): #show's everything that is inside the folder (os.listdir)
            if files.endswith(".png"): # look for jpg extensions
                weblogo_jpg_list.append(files) # put all the jpg in a list

            best_match_wl = weblogo_jpg_list[0] # thinking that the first jpg is the most accurate add this to a new var
            weblogo_jpg_list = [] # clear the list
        return best_match_wl

    def generate_tarfile(self):
        """
        Generates a tarfile based on the output from the meme command
        """
        # declaring the filename for tar
        tar_filepath = f"{output_path_meme}.tar"
        file = tarfile.open(tar_filepath, "w")

        # defines extension
        ext = (".png", ".eps", ".html", ".txt", "xml")
        files = os.listdir(output_path_meme)

        # listing the files in tar
        for filename in files:
            file.add(f"{output_path_meme}/{filename}", filename)
    
    def plot_graph(self):
        """
        Function to make a plot with the gathered data from the meme.html or meme.xml files.
        """
        pass



def html_output_file_mover():
    """
    Function to move the generated output file to the template dir so it can be displayed.
    Also it moves the generated sequence logo to 
    """
    try: # Try to move the generated meme output to the template dir to dispaly, if the content exists.
        shutil.move(WORKING_DIR / r"User_output/meme/meme.html", WORKING_DIR / r"templates/meme.html")
    except:
        print("Meme not used, quitting...")

    try: # Try to move the generated Fimo output to the template dir to dispaly, if the content exists.
        shutil.move(WORKING_DIR / r"User_output/fimo/fimo.html", WORKING_DIR / r"templates/fimo.html")
    except:
        print("Fimo not used, quitting...")

def memelogo_mover():
    # was totatally jarno
    try:
        shutil.move(WORKING_DIR / r"User_output/meme/logo1.png", WORKING_DIR / r"static/raplace.png")
    except:
        print("Meme not used, quitting...")
    return

        
def extension_check(fastafile):
    """made this path checker again re test if it works
    :param: fastafile
    :return: True or false"""
    if os.path.splitext(fastafile.name)[1] == ".fasta":
        return True
    else:
        return False
    
def is_id(line):
        return line[0] == ">"

def is_multifasta(fastafile):
    """
    Detects whether a file is fasta or multifasta
    :param str fastafile: the filepath of the fastafile you want to check
    """
    with open(fastafile, "r") as fasta:
        return len(list(filter(is_id,fasta))) >= 2
    
def xml_parser():
    motif_dict = {}
    tree = ET.parse(WORKING_DIR / "User_output/meme/meme.xml")
    root = tree.getroot()
    meme_version = (root.attrib["version"]) # meme version used.
    for motifs in root.findall("motifs"):
        for index,motif in enumerate(motifs):
            print(f'{motif.attrib["id"]} with a P-value of {motif.attrib["p_value"]} motif width: {motif.attrib["width"]}') # print-f with same information as the motif_dict.
            motif_dict[motif.attrib["id"]] = (motif.attrib["p_value"], motif.attrib["width"], motif.attrib["sites"], motif.attrib["e_value"], f"logo_{index}.png") # Dict with as key the motif id (number) and p-value as value.
        
    for index, i in enumerate(motif_dict, start=1): # demo how to get the data from the dict
        # motif_dict: first position: motif number. second position: motif width. third position: sites
        print(f"motif number {index} p-value and width: {motif_dict[i]}")
    
    return motif_dict


    # print(motif_dict)







# Test functions below:

def receive_input():
    """
    Variables collected from the website.
    """

    # Running the tools using the classes.
    meme_test = Meme(max_amount_of_motifs, max_motif_size, min_motif_size, alphabet, input_sequence_path_meme, output_path_meme) # Make Meme instance
    meme_test.add_to_path() # Check if meme is in path, otherwise add
    meme_test.run()
    print(str(meme_test)) # print information about the meme_test object.

    # meme_test.add_to_path()
    #
    # Fimo test:
    # fimo_test = Fimo(database_to_use, use_default_p_value, p_value, input_motif_file, input_sequence_path_fimo, output_path_fimo)
    # fimo_test = Fimo(database_to_use, use_default_p_value, p_value, input_motif_file, input_sequence_path_fimo, output_path_fimo)
    #
    # fimo_test.run() # execute the commandline tool using the object fimo_test.
    # print(str(fimo_test)) # print information from the def __str__ function in the Meme class.

    return database_to_use, use_default_p_value, p_value, max_amount_of_motifs, max_motif_size, min_motif_size, alphabet


def input_commands():

    fimo_command = "fimo --oc <OUTPUT_LOCATION> --verbosity 1 --bgfile --nrdb-- --thresh 1.0E-4 <Motif_file_location> <Fasta_file_location>"
    meme_command = "meme '/home/floris/OneDrive_FLORIS/Hanze_Bioinformatica/Jaar_1/Projecten/PAM_Scoring_matrix/DATA/meme_sample_sequences' -dna -oc ~/Documenten/OUTPUT_DATA/MEME/ -time 14400 -mod zoops -nmotifs 3 -minw 6 -maxw 50 -objfun classic -revcomp -markov_order 0"

    return fimo_command, meme_command


def process_commands(fimo_command, meme_command):
    pass
    # meme_output = subprocess.run([meme_command], shell=True) # , capture_output=True, text=True
    # fimo_output = subprocess.run([fimo_command], shell=True)

    # output_meme = meme_output.stdout
    # output_fimo = fimo_output.stdout

    # print(f"print: {output_meme} type: {type(output_meme)}")
    # print(f"output fimo: {fimo_output} type: {type(output_fimo)}")


if __name__ == "__main__":
    database_to_use, use_default_p_value, p_value, max_amount_of_motifs, max_motif_size, min_motif_size, alphabet = receive_input()
    fimo_command, meme_command = input_commands()
    #process_commands(fimo_command, meme_command)

