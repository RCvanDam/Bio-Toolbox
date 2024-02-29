**Transcription factor binding site recongition tool**


## **Instalation Guide** ##
To use this website and python script, the MEME suite is needed. 
It can be compiled from source as described below. 
Execute the folowing commands:
<p> 
Download the meme-x.x.x.tar.gz file from the following website: <br />
https://meme-suite.org/meme/doc/download.html <br />
tar zxf meme-5.5.5.tar.gz # to decompress the files <br />
          cd meme-5.5.5 # to move to the directory <br />
          ./configure --prefix=$HOME/meme --enable-build-libxml2 --enable-build-libxslt # to configure for the os <br/>
           make # to compile <br />
          make install # to install <br />
To add this tool to the PATH variable: <br />
export PATH=$HOME/meme/bin:$HOME/meme/libexec/meme-5.5.5:$PATH <br />
</p>

<p>
**Commandline Example:** <br /> 
meme <INPUT_FILE_LOCATION> -dna -oc <OUTPUT_LOCATION> -time 14400 -mod zoops -nmotifs 3 -minw 6 -maxw 50 -objfun classic -revcomp -markov_order 0 <br /> 
The flags can be changed, for example: -dna can be -rna or -protein and -nmotifs 3 can be changed to any arbitrary number of motifs that the program should find (it stops looking when the number is reached) <br />
</p>

<p>
**System Requirements:** <br />
Any python compatible x86 or x64 computer with the MEME Suite installed. <br />
RAM requirements depend on the size of the input files (Motif file and the sequence that needs to be scanned) <br /> 
</p>
.

**Goal of the project**

****

****

6. references

