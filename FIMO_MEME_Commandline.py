
"""
MemeSuite backend for website
Author: Floris M
Date: 7-03-2024
Version: 0.01

"""

import sys
import subprocess # om terminal commando's uit te voeren in python 


def input_commands():
    
    fimo_command = "fimo 'input location'" 
    meme_command = "meme '/home/floris/OneDrive_FLORIS/Hanze_Bioinformatica/Jaar_1/Projecten/PAM_Scoring_matrix/DATA/meme_sample_sequences' -dna -oc ~/Documenten/OUTPUT_DATA/MEME/ -time 14400 -mod zoops -nmotifs 3 -minw 6 -maxw 50 -objfun classic -revcomp -markov_order 0"

    return fimo_command, meme_command


def process_commands(fimo_command, meme_command):
    meme_output = subprocess.run([meme_command], shell=True) # , capture_output=True, text=True
    fimo_output = subprocess.run([meme_command], shell=True)

    output_meme = meme_output.stdout
    output_fimo = fimo_output.stdout

    print(f"print: {output_meme} type: {type(output_meme)}")
    print(f"output fimo: {fimo_output} type: {type(output_fimo)}")


if __name__ == "__main__":
    fimo_command, meme_command = input_commands()
    process_commands(fimo_command, meme_command)

