import pytest
from ..source import my_functions as myfuncs

def test_add():
    r=myfuncs.add(1,4)
    assert r==5

def test_divide():
    result = myfuncs.divide(10,5)
    assert result==2

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        myfuncs.divide(10,0)

#@pytest.fixture
#@pytest.mark.parametrize