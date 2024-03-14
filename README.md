# **MEFIM-FindR** #
**version 0.01**
## **Authors** ##
<p>
Floris Menninga: Main programmer Tool <br>
Ruben van Dam: Main Tool intergration programmer <br>
Tai Vo: Main back-end programmer <br>
Jarno Duiker: Main Front-end programmer 
</p>

 ## **Purpose of our website and tool**
MemeSuite is a collection of tools with the encompassing goal of transcription factor binding site recognition and the discovery of new binding sites.
To recognize TF(transcription factor) binding sites, one can use the FIMO tool. FIMO is used to scan for the presence of known transcription factor motifs, a list of motifs has to be given in order to search for them.

The other tool that we implemented on the website is MEME. This tool is used to find novel transcription factor binding sites. For this, the user has to
input a multi-fasta sequence with the sequences that the tool should use to find motifs. A motif is a short nucleotide pattern that consists of about 4 to 20 nucleotides.<br>

The sequence of this motif is not always the same but there are nucleotides at every position in this short sequence that have a higher likelihood of occurring at that place. The chance of what nucleotide occurs at what position can be displayed using a SequenceLogo. See the example SequenceLogo below.<br>
![Example Sequence logo](Sequence_logo.png)
<br>
In the motif sequence, the nucleotide for every position in the sequence is displayed. When there are more occurrences of a particular nucleotide, this nucleotide will be on top of and bigger than the lesser frequent occurring nucleotides.

## **Instalation Guide** ##
Note: This manual was tested with MemeSuite version 5.5.5. Newer versions may not work in the same way.<br><br>
To use this website and python script, the MEME suite is needed. 
It can be compiled from source as described below. 
Execute the folowing commands:
<p> 
Download the meme-x.x.x.tar.gz file from the following website: <br />
<a href="https://meme-suite.org/meme/doc/download.html">https://meme-suite.org/meme/doc/download.html<a><br />
<code> tar zxf meme-5.5.5.tar.gz </code> # to decompress the files <br />
         <code> cd meme-5.5.5 </code> # to move to the directory <br /> </code>
         <code> ./configure --prefix=$HOME/meme --enable-build-libxml2 --enable-build-libxslt </code> # to configure for the os <br/>
         <code>  make </code> # to compile <br />
         <code> make install </code> # to install <br />
To add this tool to the PATH variable: <br />
<code> export PATH=$HOME/meme/bin:$HOME/meme/libexec/meme-5.5.5:$PATH  <code><br />
</p>


## **System Requirements:** ##
<p>
Note: MemeSuite can be compiled from source on linux or run in a docker container on MacOS, Windows or linux
Any python compatible x86 or x64 computer with the MEME Suite installed. <br />
RAM requirements depend on the size of the input files (Motif file and the sequence that needs to be scanned) <br /> 
</p>
<br>


## **Commandline Example:** ##
<p>
meme <INPUT_FILE_LOCATION> -dna -oc <OUTPUT_LOCATION> -time 14400 -mod zoops -nmotifs 3 -minw 6 -maxw 50 -objfun classic -revcomp -markov_order 0 <br />
The flags can be changed, for example: -dna can be -rna or -protein and -nmotifs 3 can be changed to any arbitrary number of motifs that the program should find (it stops looking when the number is
reached) <br />
</p>

## **Contact** ##
<p> For feedback, bugs and other problems. Contact us! <br>
Tai Vo git: MoonCake98 <br>
Jarno Duiker git: azzipxonraj <br>
Ruben van Dam git: RCvanDam <br>
Floris Menninga git: Fl-ris </p>

## **Refrences on 29/02/2024** ##
**TOOLS**
<p>
MEME Suite. (z.d.). https://meme-suite.org/meme/doc/overview.html
</p>
