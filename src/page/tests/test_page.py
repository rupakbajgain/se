import pytest
from ..source import page

from pytest_mock import MockerFixture

@pytest.fixture
def my_page():
    return page.Page('https://example.com/1')

def test_links(mocker: MockerFixture, my_page):
    import requests
    request = mocker.patch('requests.get')
    class MockResult:
        content = b'<title>test</title><a href="abc">link</a>'
    request.return_value = MockResult()

    r = my_page.fetch()
    assert b'test' in r
    soup = my_page.get_soup()
    assert soup.title.string == 'test'
    links = my_page.get_all_links()
    assert 'https://example.com/abc' in links
    links2 = my_page.get_filtered_links()
    assert len(links2)==0#same page so no diff

def test_navigation(my_page):
    p2 = my_page.goto('../2')
    assert p2.url == 'https://example.com/2'
    assert p2.get_last_history() == my_page.url