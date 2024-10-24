import pytest
from ..source import my_functions as myfuncs
import json
import os
from ...config import getConfig

@pytest.fixture
def prof():
    with open(os.path.join(os.path.dirname(__file__),'in.json')) as f:
        return json.load(f)

@pytest.fixture
def paper_snippets():
    with open(os.path.join(os.path.dirname(__file__),'test_in.txt')) as f:
        return f.read()


def test_mail(paper_snippets,prof):
    config = getConfig()
    user=config['basic']['DEFAULT_USER']#def
    config.set('basic','USER',user)
    config.read(f'assets/configs/{user}.ini')

    #check basic criteria so email is mostly valid without editing
    r=myfuncs.docs_to_email(paper_snippets,prof)
    assert '[' not in r[0]
    assert ']' not in r[0]
    assert r