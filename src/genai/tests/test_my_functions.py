import pytest
from ..source import my_functions as myfuncs

def test_genai():
    r=myfuncs.get_response('What is capital of nepal?')
    assert 'Kathmandu' in r
