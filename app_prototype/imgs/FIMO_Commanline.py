
"""
MemeSuite backend for website
Author: Floris M
Date: 7-03-2024
Last updated: 21-03-2024

Version: 0.05

"""


import subprocess # om terminal commando's uit te voeren in python 


# Global test variables (should be replaced by the ones given back by the webserver.)

# Variables for FIMO
database_to_use = False # Name of the database.
use_default_p_value = True # True or false
p_value = 0.0001 # float, default is 0.0001.
input_motif_file = "/home/floris/Documenten/Data_set/Motifs/motif_databases/MOUSE/HOCOMOCOv11_full_MOUSE_mono_meme_format.meme" 
input_sequence_path_fimo = "/home/floris/Documenten/Data_set/Motifs/meme_sample_sequences.fasta"
output_path_fimo = "~/Documenten/OUTPUT" # (Temporary) storage place for the generated files. 


# Variables for MEME
max_amount_of_motifs = 0 # max abount of motif to look for, program stops looking if the number is exceeded.
max_motif_size = 0 # max length of the motifs.
min_motif_size = 0 
alphabet = "DNA" # Nucleotide alphabet to use: RNA, DNA or protein.
input_sequence_path_meme = ""
output_path_meme = ""
path_memesuite_export = "export PATH=/opt/local/bin:/opt/local/libexec/meme-5.5.5:$PATH"


class Fimo: 
    """
    The Fimo class serves the purpose of running the Fimo tool after the parameters from the website are collected.
    """

    def __init__(self, database_to_use, use_default_p_value, p_value):
        self.database_to_use = database_to_use
        self.use_default_p_value = use_default_p_value
        self.p_value = p_value
        self.input_motif_file = input_motif_file # to-do 
        self.input_sequence_path_fimo = input_sequence_path_fimo
        self.ouput_path_fime

    
    def __str__(self):
        return f"Database used: {database_to_use}, Default p-value used?: {use_default_p_value}, P-value: {p_value}"
    
    def run(self):
        if database_to_use: # If the user selected one of the databases instead of a motif file. 
            pass
        else: # if not: use a given motif file.
            fimo_command = "fimo --oc {} --verbosity 2 --bgfile --nrdb-- --thresh {} {} {}".format(output_path_fimo, p_value, input_motif_file, input_sequence_path_fimo)

        fimo_output = subprocess.run([fimo_command], shell=True)
        output_fimo = fimo_output.stdout
        print(output_fimo) # should be redirected to the ouput display in the website. 


class Meme:

    def __init__(self, max_amount_of_motifs, max_motif_size, min_motif_size, alphabet, ):
        self.max_amount_of_motifs = max_amount_of_motifs
        self.max_motif_size = max_motif_size
        self.min_motif_size = min_motif_size
        self.alphabet = alphabet

    
    def __str__(self):
        return f"Max amount of motifs: {self.max_amount_of_motifs}, Max motif size: {self.max_motif_size}, Min motif size: {self.min_motif_size}, Alphabet used: {self.alphabet}."
    

    def add_to_path(self):
        print("in Path?")
        meme_in_path = subprocess.run("echo $PATH", shell=True, text=True, capture_output=True).stdout
        print(meme_in_path)
        if "meme" in meme_in_path:
            print("Memsuite in path")
        else:
            print("memesuite not in path, adding now...")
            subprocess.run("export PATH=/opt/local/bin:/opt/local/libexec/meme-5.5.5:$PATH", shell=True, text=True)



    def run(self): # add commandline execution using the user given parameters.
      #  meme_command_test = "meme '/home/floris/Documenten/Data_set/DATA/meme_sample_sequences' -dna -oc ~/Documenten/OUTPUT_DATA/MEME/ -time 14400 -mod zoops -nmotifs 3 -minw 6 -maxw 50 -objfun classic -revcomp -markov_order 0"
        
        meme_command_test = "meme {} {} -oc {} -time 14400 -mod zoops {} -minw 6 -maxw 50 -objfun classic -revcomp -markov_order 0".format(input_sequence_path_meme, alphabet, output_path_meme, max_amount_of_motifs)
        meme_output = subprocess.run([meme_command_test], shell=True)
        output_meme = meme_output.stdout
        print(output_meme) # should be redirected to the ouput display in the website. 


def fasta_header_control():

    with open(fasta_file, "r") as fasta:
        counter = 0
        multifasta = False
        for i in fasta:
            if ">" in i:
                counter += 1
            if counter >= 2:
                multifasta = True
                print(multifasta)
                return multifasta
        return multifasta

def receive_input():
    """
    Variables collected from the website. 

    """

    # Running the tools using the classes.
    meme_test = Meme(max_amount_of_motifs, max_motif_size, min_motif_size, alphabet) # Make Meme instance
    meme_test.run()
    print(str(meme_test)) # print information about the meme_test object.
    meme_test.add_to_path()


    # Fimo test:
    # fimo_test = Fimo(database_to_use, use_default_p_value, p_value)
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
