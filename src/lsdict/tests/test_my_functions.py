import pytest
from ..source import my_functions as myfuncs
import os

test_dir = os.path.join(os.path.dirname(__file__),'test_helper')

def test_list():
    r=myfuncs.list_dict(test_dir)
    assert r[0][0] in ['t1','t2']
    assert r[1][0] in ['t1','t2']

def test_get_info():
    r=myfuncs.get_info(test_dir+'/t1.py')
    assert 'sdafet' in r
    assert not '#' in r
    r=myfuncs.get_info(test_dir+'/t2.py')
    assert 'test2ss' in r

def test_main_loader():
    main=myfuncs.get_main(test_dir+'/t1.py')
    o=main()
    assert o==1
    main=myfuncs.get_main(test_dir+'/t2.py')
    o=main()
    assert o==2
