"""
Python unit-test for the Homepage, Memepage and Fimopage. 
Date: 25-03-2024
Author: Floris M

"""


import unittest
from FIMO_MEME_Commandline import is_multifasta, extension_check



def test_fimo_backend():
    pass


def test_meme_backend():
    pass

def test_multi_fasta(fasta, multifasta):
    is_multifasta(fasta, multifasta)


def test_extention():
    assert extension_check()
