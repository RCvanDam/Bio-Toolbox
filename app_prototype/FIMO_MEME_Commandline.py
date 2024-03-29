
"""
MemeSuite backend for website
Author: Floris M, Ruben van Dam
Date: 7-03-2024
Last updated: 28-03-2024

Version: 0.12

"""

import subprocess # To execute terminal command's on the computer.
import os
import tarfile
import shutil

# Global test variables (should be replaced by the ones given back by the webserver.)
working_dir = os.path.dirname(os.path.realpath(__file__)) # to check current dir
print(working_dir)


# Test variables for FIMO
database_to_use = False # Name of the database.
use_default_p_value = True # True or false
p_value = 0.0001 # float, default is 0.0001.
input_motif_file = "{}/Motif_databases/SwissRegulon_e_coli.meme".format(working_dir)
input_sequence_path_fimo = "{}/meme_sample_sequences.fasta".format(working_dir) # replace with relative path.
output_path_fimo = "{}/User_output/fimo".format(working_dir) # (Temporary) storage place for the generated files. 


# Test variables for MEME
max_amount_of_motifs = 20 # max abount of motif to look for, program stops looking if the number is exceeded.
max_motif_size = 8 # max length of the motifs.
min_motif_size = 3 
alphabet = "dna" # Nucleotide alphabet to use: RNA, DNA or protein.
input_sequence_path_meme = "{}/meme_sample_sequences.fasta".format(working_dir)
output_path_meme = "{}/User_output/meme".format(working_dir)
home_path = subprocess.run("echo $HOME", shell=True, text=True, capture_output=True).stdout.rstrip()


class Fimo:
    """
    The Fimo class serves the purpose of running the Fimo tool after the parameters from the website are collected.

    :param database_to_use: The motif file to use when the user doesn't provide their own.
    :param use_default_p_value: True or False, whether or not to use the default P-value.
    :param p_value: If chosen, the custom P-value. 
    """

    def __init__(self, database_to_use, use_default_p_value, p_value, input_motif_file, input_sequence_path_fimo, output_path_fimo):
        self.database_to_use = database_to_use
        self.use_default_p_value = use_default_p_value
        self.p_value = p_value
        self.input_motif_file = input_motif_file
        self.input_sequence_path_fimo = input_sequence_path_fimo
        self.output_path_fimo = output_path_fimo

    def __str__(self):
        """
        Returns information about the created object. 
        """
        return f"Database used: {database_to_use}, Default p-value used?: {use_default_p_value}, P-value: {p_value}"

    def run(self):
        """
        Using the ".run()" method, the Fimo tool will be run. No parameters needed because they were already given when the class was initialized. 
        """


        if database_to_use: # If the user selected one of the databases instead of a motif file. 
            pass # add logic to select database depending on the user selection.
        else: # if not: use a given motif file.
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
        self.max_amount_of_motifs = max_amount_of_motifs
        self.max_motif_size = max_motif_size
        self.min_motif_size = min_motif_size
        self.alphabet = alphabet
        self.input_sequence_path_meme = input_sequence_path_meme
        self.output_path_meme = output_path_meme
        self.new_env = None
    
    def __str__(self):
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
        if is_multifasta(input_sequence_path_meme):
            # meme_command_test = "meme '/home/floris/Documenten/Data_set/DATA/meme_sample_sequences' -dna -oc ~/Documenten/OUTPUT_DATA/MEME/ -time 14400 -mod zoops -nmotifs 3 -minw 6 -maxw 50 -objfun classic -revcomp -markov_order 0"
            meme_command_test = "meme {} -{} -oc {} -time 14400 -mod zoops -nmotifs {} -minw 6 -maxw 50 -objfun classic -revcomp -markov_order 0".format(
            input_sequence_path_meme, alphabet.lower(), output_path_meme, max_amount_of_motifs)
            print(f"Running command: {meme_command_test}\nwith PATH: {self.new_env['PATH']}\n")

            meme_output = subprocess.run([meme_command_test],  executable="/bin/sh", shell=True, text=True, env=self.new_env)
            output_meme = meme_output.stdout
            print(output_meme) # should be redirected to the ouput display in the website.
            self.generate_tarfile()
        else:
            print("To use the MEME command, please use a multi-fasta file as input")


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
        for x in files:
            file.add(f"{output_path_meme}/{x}", x)

        
        shutil.rmtree(f"{output_path_meme}", ignore_errors=True)
        
def extension_check(fastafile):
    """made this path checker again re test if it works
    :param: fastafile
    :return: True or false"""
    if os.path.splitext(fastafile)[1] == ".fasta":
        return True
        
def is_multifasta(fastafile: str):
    """
    Detects whether a file is fasta or multifasta
    :param str fastafile: the filepath of the fastafile you want to check
    """
    with open(fastafile, "r") as fasta:
        counter = 0

        # Count fastas in fasta file
        for line in fasta:
            if ">" in line:
                counter += 1
            if counter >= 2:
                return True

        # Reached end of fasta file, with counter < 2
        return False


def receive_input():
    """
    Variables collected from the website.
    """

    # Running the tools using the classes.
    meme_test = Meme(max_amount_of_motifs, max_motif_size, min_motif_size, alphabet, input_sequence_path_meme, output_path_meme) # Make Meme instance
    meme_test.add_to_path() # Check if meme is in path, otherwise add
    meme_test.run()
    print(str(meme_test)) # print information about the meme_test object.

    #meme_test.add_to_path()

    # Fimo test:
    # fimo_test = Fimo(database_to_use, use_default_p_value, p_value, input_motif_file, input_sequence_path_fimo, output_path_fimo)
    # fimo_test = Fimo(database_to_use, use_default_p_value, p_value, input_motif_file, input_sequence_path_fimo, output_path_fimo)

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
    
