## Transcription factor binding site seeker ##
> Date: 06-04-2024 \
> Authors: Tai V and Floris M


## Running app.py ##
.


## Using the MEME tool ##
MEME is a tool used for finding motifs in a sequence file (fasta), the tool should be presented one or multiple sequences in a fasta, multi-fasta or plain-text. The output of the program is one or more sequence logo pictures, the full list of these motifs is also saved in a seperate file (.html) and the sequence logo picture can be downloaded for later reference using the "Download sequenceLogo" button.

### <b>For MEME the parameters for the user to fill in:</b> ###
There are a couple of parameters that should be given to the software like max amount of motifs to look for, max motif size and minimum motif size. The alphabet should also be specified (DNA, RNA or protein).



## Using the FIMO tool ##
FIMO is a tool used for finding motif occurences in a geven fasta sequence.
FIMO requires a multi-fasta and a motif file as input. The sequences in the multi-fasta will only be checked for motifs that are present in this motif file.
This motif file can be either .meme or .dreme output file from a motif discovery tool like MEME, STREME or DREME (other tools similar to MEME) and is formatted as a MEME motif format.
Just like with MEME, the results of FIMO are returned with a p-value. The user can also filter the output so that results that are not statistically significant are ignored.

### <b>For FIMO the parameters for the user to fill in:</b> ###
Reject matches with a higher P-value than the given value (corresponds to commandline argument: --thresh) This last option is to reject matches with a lesser statistical likelihood of being a good match for the given motif. The program also has a internal P-value cut-off for when the amount of possible matches exeeds a certain number, this value is not configurable. The final parameter is: Database, With this option, the user can specify whith wich database the mulit-fasta should be scanned when there is no motif file given. (Using a motif file overrides this option)

