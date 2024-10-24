import pytest
from ..source import my_functions as myfuncs
import json
import os

@pytest.fixture
def prof():
    with open(os.path.join(os.path.dirname(__file__),'in.json')) as f:
        return json.load(f)

def test_prof_data(prof):
    r=myfuncs.get_prof_datas(prof)
    assert isinstance(r, list)

#@pytest.fixture
#@pytest.mark.parametrize