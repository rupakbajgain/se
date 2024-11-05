import pytest
from ..source import my_functions as myfuncs
import configparser

def test_persist():
    @myfuncs.persist('test_count')
    def persist_x(c):
        return c
    assert persist_x(5) == 5
    #clear
    assert myfuncs.clear_persist('test_count')(5)
