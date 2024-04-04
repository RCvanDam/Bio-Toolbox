"""
Python unit-test for the Homepage, Memepage and Fimopage. 
Date: 25-03-2024
Author: Floris M

"""


import pytest
import html5lib # for testing the website
import os
from FIMO_MEME_Commandline import is_multifasta, extension_check
#import app.py

WORKING_DIR = os.path.dirname(os.path.realpath(__file__)) # to check current dir


def test_fimo_backend():
    pass


def test_meme_backend():
    pass


def test_extention():
    # .fasta extention
    assert extension_check(WORKING_DIR + "app_prototype/eme_sample_sequences.fasta") == True 
    # wrong extention
    assert extension_check(WORKING_DIR + "unit_tests/test_fasta_wrong_extention.fastaaa") == False


def test_multi_fasta():
   # Multi-fasta test:
   assert is_multifasta(WORKING_DIR + "/meme_sample_sequences.fasta")  == True
   # Fasta test:
   assert is_multifasta(WORKING_DIR + "/test_fasta_wrong_extention.fastaaa")  == False
