#!/usr/bin/env bash

# Download the memeSuite software.
wget https://meme-suite.org/meme/meme-software/5.5.5/meme-5.5.5.tar.gz

# untar the folder in the home directory.
tar -xvzf meme-5.5.5.tar.gz -C ~

cd ~/meme-5.5.5

# Configure for compilation
./configure --prefix=$HOME/meme --enable-build-libxml2 --enable-build-libxslt

# Compile with as many cores as the system has.
make -j$(nproc)

# Install
make install

# Temporarily add meme to the $PATH.
export PATH=$HOME/meme/bin:$HOME/meme/libexec/meme-5.5.5:$PATH

#
# THIS IS A TEST SCRIPT, DON'T EXCECUTE!!
#

# Prerequisite software:
#
#     Perl
#     Python
#     zlib
#     Ghostscript
#     Assorted common utilities
#
