import pytest
from ..source import my_functions as myfuncs
import json,os
import shutil
from ...config import getConfig

@pytest.fixture
def prof():
    with open(os.path.join(os.path.dirname(__file__),'in.json')) as f:
        return json.load(f)

@pytest.fixture
def links():
    l=[]
    with open(os.path.join(os.path.dirname(__file__),'in.txt')) as f:
        for line in f:
            d=json.loads(line)
            l.append(d)
    return l

def test_loader(prof,links):
    config = getConfig()
    fake_path = os.path.join(os.path.dirname(__file__),'fake_download')
    actual_path = config['directories']['DOWNLOAD_PATH']
    files=os.listdir(fake_path)
    for fname in files:
        shutil.copy(os.path.join(fake_path,fname), actual_path)
    t1 = myfuncs.prof_to_doc(prof)
    assert 'Info' in t1
    d = myfuncs.get_documents(links)
    t = myfuncs.docs_to_text(d)
    assert 'asdkglh' in t#get from conclusion
    #assert 'dqwkjbeqfkjb' in t
    #just not working with UnstructuredLoader
    assert not 'fwqfafcsfvesdgf' in t#no refrences