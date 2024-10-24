import pytest
from ..source import my_functions as myfuncs
import json
import os
from ...config import getConfig

@pytest.fixture
def prof():
    with open(os.path.join(os.path.dirname(__file__),'in.json')) as f:
        return json.load(f)

@pytest.mark.skip(reason="Actually sends mail")
def test_automail(prof):
    config = getConfig()
    user=config['basic']['DEFAULT_USER']#def
    config.set('basic','USER',user)
    config.read(f'assets/configs/{user}.ini')

    assert myfuncs.automail(prof,True)