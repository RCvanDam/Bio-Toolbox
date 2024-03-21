
"""
MemeSuite backend for website
Author: Floris M
Date: 7-03-2024
Last updated: 21-03-2024

Version: 0.05

"""


import subprocess # om terminal commando's uit te voeren in python 


class Fimo:
    """
    The Fimo class serves the purpose of running the Fimo tool after the parameters from the website are collected.

    
    """

    def __init__(self, database_to_use, use_default_p_value, p_value):
        self.database_to_use = database_to_use
        self.use_default_p_value = use_default_p_value
        self.p_value = p_value

    def __str__(self):
        return f"Database used: {database_to_use}, Default p-value used?: {use_default_p_value}, P-value: {p_value}"
    
    def run(self):
        if database_to_use: # If the user selected one of the databases instead of a motif file. 
            pass
        else: # if not: use a given motif file.
            fimo_command = "fimo --oc {output_path_fimo} --verbosity 1 --bgfile --nrdb-- --thresh {p_value} {input_motif_file} {input_sequence_path_fimo}".format()

        fimo_output = subprocess.run([fimo_command], shell=True)
        output_fimo = fimo_output.stdout
        print(output_fimo) # should be redirected to the ouput display in the website. 


class Meme:

    def __init__(self, max_amount_of_motifs, max_motif_size, min_motif_size, alphabet):
        self.max_amount_of_motifs = max_amount_of_motifs
        self.max_motif_size = max_motif_size
        self.min_motif_size = min_motif_size
        self.alphabet = alphabet

    
    def __str__(self):
        return f"Max amount of motifs: {self.max_amount_of_motifs}, Max motif size: {self.max_motif_size}, Min motif size: {self.min_motif_size}, Alphabet used: {self.alphabet}."


    def run(self): # add commandline execution using the user given parameters.
      #  meme_command_test = "meme '/home/floris/Documenten/Data_set/DATA/meme_sample_sequences' -dna -oc ~/Documenten/OUTPUT_DATA/MEME/ -time 14400 -mod zoops -nmotifs 3 -minw 6 -maxw 50 -objfun classic -revcomp -markov_order 0"
        
        meme_command_test = "meme {input_sequence_path_meme} {alphabet} -oc {output_path_meme} -time 14400 -mod zoops {max_amount_of_motifs} -minw 6 -maxw 50 -objfun classic -revcomp -markov_order 0".format()
        meme_output = subprocess.run([meme_command_test], shell=True)
        output_meme = meme_output.stdout
        print(output_meme) # should be redirected to the ouput display in the website. 

        



def receive_input():
    """
    Variables collected from the website. 

    """

    # Variables for FIMO
    database_to_use = "" # Name of the database.
    use_default_p_value = True # True or false
    p_value = 0.0001 # float, default is 0.0001.

    # Variables for MEME
    max_amount_of_motifs = 0 # max abount of motif to look for, program stops looking if the number is exceeded.
    max_motif_size = 0 # max length of the motifs.
    min_motif_size = 0 
    alphabet = "DNA" # Nucleotide alphabet to use: RNA, DNA or protein.


    # Running the tools using the classes.
    meme_test = Meme(max_amount_of_motifs, max_motif_size, min_motif_size, alphabet) # Make Meme instance
    print(str(meme_test)) # print information about the meme_test object.
    meme_test.run()


    return database_to_use, use_default_p_value, p_value, max_amount_of_motifs, max_motif_size, min_motif_size, alphabet


def input_commands():
    
    fimo_command = "fimo --oc <OUTPUT_LOCATION> --verbosity 1 --bgfile --nrdb-- --thresh 1.0E-4 <Motif_file_location> <Fasta_file_location>"
    meme_command = "meme '/home/floris/OneDrive_FLORIS/Hanze_Bioinformatica/Jaar_1/Projecten/PAM_Scoring_matrix/DATA/meme_sample_sequences' -dna -oc ~/Documenten/OUTPUT_DATA/MEME/ -time 14400 -mod zoops -nmotifs 3 -minw 6 -maxw 50 -objfun classic -revcomp -markov_order 0"

    return fimo_command, meme_command


def process_commands(fimo_command, meme_command):
    meme_output = subprocess.run([meme_command], shell=True) # , capture_output=True, text=True
    fimo_output = subprocess.run([fimo_command], shell=True)

    output_meme = meme_output.stdout
    output_fimo = fimo_output.stdout

    print(f"print: {output_meme} type: {type(output_meme)}")
    print(f"output fimo: {fimo_output} type: {type(output_fimo)}")



if __name__ == "__main__":
    database_to_use, use_default_p_value, p_value, max_amount_of_motifs, max_motif_size, min_motif_size, alphabet = receive_input()
    fimo_command, meme_command = input_commands()
  #  process_commands(fimo_command, meme_command)
