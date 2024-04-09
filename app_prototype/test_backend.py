"""
Python unit-test for the Homepage, Memepage and Fimopage. 
Date: 25-03-2024
Author: Floris M

"""

import pytest
import html5lib # for testing the website
import os # for the working_dir path
from FIMO_MEME_Commandline import is_multifasta, extension_check
# from app_prototype.FIMO_MEME_Commandline import is_multifasta, extension_check

from app import app
from pathlib import Path

# WORKING_DIR = Path(os.path.dirname(os.path.realpath(__file__))) # to check current dir
WORKING_DIR = Path.cwd()
print(type(WORKING_DIR))
# print(WORKING_DIR)


def test_fimo_backend():
    pass


def test_meme_backend():
    pass


def test_extention():
    """
    Extension function test to check if the function can distinguise between files with one of the allowed
    extentions like .fasta or .faa.
    """
    # .fasta extention
    assert extension_check(WORKING_DIR / "app_prototype" / "meme_sample_sequences.fasta") == True 
    # wrong extention
    assert extension_check(WORKING_DIR / "unit_tests" / "test_fasta_wrong_extention.fastaaa") == False


def test_multi_fasta():
   """
   Function test to check if the "is_multifasta" function can detect if a sequence is a fasta or multifasta. 
   """
   # Multi-fasta test:
   assert is_multifasta(WORKING_DIR / "meme_sample_sequences.fasta")  == True
   # Fasta test:
   assert is_multifasta(WORKING_DIR / "test_fasta_wrong_extention.fastaaa")  == False


@pytest.fixture
def client():
    """
    
    """
    return app.test_client()


@pytest.mark.parametrize('web_status_code', [
    #  '/' # gets redirected to "/about"
     '/fimo',
     '/meme',
     '/about'

])
# test for http status code:
def test_status_code(client, web_status_code):
    response = client.get(web_status_code)
    assert response.status_code == 200
    

# Old tests from before parametrization.
# def test_meme(client):
#     response = client.get("/meme")
#     assert response.status_code == 200

# def test_fimo(client):
#     response = client.get("/fimo")
#     assert response.status_code == 200


@pytest.mark.parametrize('uri', [
     '/',
    '/form',
    '/fimo',
    '/meme',
    '/about'

])

def test_html_parse_meme(client, uri):
    response = client.get(uri)
    assert response.status_code == 200
    try:
        parser = html5lib.HTMLParser(strict=False, namespaceHTMLElements=False)
        htmldoc = parser.parse(response.data)
    except html5lib.html5parser.ParseError as error:
        pytest.fail(f'{error.__class__.__name__}: {str(error)}', pytrace=False)


@pytest.mark.parametrize('uri', [
     '/',
    '/form',
    '/fimo'
    '/meme'

])

def test_html_parse_fimo(client, uri):
    response = client.get("/fimo")
    assert response.status_code == 200
    try:
        parser = html5lib.HTMLParser(strict=False, namespaceHTMLElements=False)
        htmldoc = parser.parse(response.data)
    except html5lib.html5parser.ParseError as error:
        pytest.fail(f'{error.__class__.__name__}: {str(error)}', pytrace=False)
    forms = htmldoc.findall('./body/div/div/div/div/form')
    assert len(forms) == 1
    # form = forms[0]
    names = set()
    # for inp in form.iter('input'):
    #     names.add(inp.attrib['name'])
    # assert names == {'course', 'teacher', 'ec'}


def test_html_parse_meme(client):
    response = client.get("/meme")
    assert response.status_code == 200
    try:
        parser = html5lib.HTMLParser(strict=False, namespaceHTMLElements=False)
        htmldoc = parser.parse(response.data)
    except html5lib.html5parser.ParseError as error:
        pytest.fail(f'{error.__class__.__name__}: {str(error)}', pytrace=False)
    forms = htmldoc.findall('./body/div/div/div/div/form')
    assert len(forms) == 1
    names = set()