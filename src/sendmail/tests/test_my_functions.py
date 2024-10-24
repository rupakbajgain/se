import pytest
from ..source import my_functions as myfuncs
from ...config import getConfig

def test_toHTML():
    config = getConfig()
    user=config['basic']['DEFAULT_USER']#def
    config.set('basic','USER',user)
    config.read(f'assets/configs/{user}.ini')

    r=myfuncs.toHTML('testMSG\n123')
    assert 'testMSG<br/>\n123' in r

def test_try_login():
    #to compensate skipped sendemail
    #just checks login with default username and password
    config = getConfig()
    user=config['basic']['DEFAULT_USER']#def
    config.set('basic','USER',user)
    config.read(f'assets/configs/{user}.ini')
    myfuncs.try_login()

@pytest.mark.skip(reason="Actually sends email") 
def test_sendEmail():
    config = getConfig()
    user=config['basic']['DEFAULT_USER']#def
    config.set('basic','USER',user)
    config.read(f'assets/configs/{user}.ini')
    r=myfuncs.send_email('hellomsg123','hello_sub','nnew234567@gmail.com')
    assert r
