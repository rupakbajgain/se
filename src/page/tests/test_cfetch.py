import pytest
from ..source import cfetch
from ...config import getConfig
import os

@pytest.fixture
def my_cfetch():
    return cfetch.CFetch('https://example.com/')

def test_head(my_cfetch):
    r = my_cfetch.head()
    assert r.status_code==200

def test_requests(my_cfetch):
    r = my_cfetch.requests_fetch()
    assert 'Example Domain' in r.decode()

def test_cfetch(my_cfetch):
    #also test playwright and cache
    config = getConfig()
    filepath = os.path.join(config['directories']['DOWNLOAD_PATH'], '182ccedb33a9e03fbf1079b209da1a31')
    if os.path.exists(filepath):
        os.remove(filepath)
    #start browser
    cfetch.start_browser()
    r = my_cfetch.fetch()
    assert 'Example Domain' in r.decode()
    cfetch.shutdown_browser()
    assert os.path.exists(filepath)
    #lets append some test content to file to make sure it is loaded instead of fetched
    testmsg = 'ffappendedtext'
    with open(filepath, "a") as myfile:
        myfile.write(testmsg)
    r = my_cfetch.fetch()
    assert testmsg in r.decode()
    os.remove(filepath)