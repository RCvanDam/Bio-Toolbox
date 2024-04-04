"""
Python unit-test for the Homepage, Memepage and Fimopage. 
Date: 25-03-2024
Author: Floris M

"""
import os
working_dir = os.path.dirname(os.path.realpath(__file__)) # to check current dir

import unittest


path = "app_prototype/FIMO_MEME_Commandline"
tool = "{}/{}".format(working_dir, path)
import "{}/{}".format(working_dir, path)



def test_fimo_backend():
    pass


def test_meme_backend():
    pass

def test_multi_fasta(fasta, multifasta):
    is_multifasta(fasta, multifasta)


    



