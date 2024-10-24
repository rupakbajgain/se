import pytest
from flask import session
from .main import app, get_user_id, get_secondary_storage

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the AutoMail' in response.data

def test_userinfo_get(client):
    response = client.get('/userinfo')
    assert response.status_code == 200
    assert b'User Information' in response.data

def test_userinfo_post_save_info(client):
    data = {
        'action': 'SaveInfo',
        'username': 'Test User',
        'email': 'test@example.com',
        'password': 'testpassword',
        'cv_location': 'assets/docs/test_cv.pdf',
        'university': 'Test University',
        'footer': 'Test Footer'
    }
    response = client.post('/userinfo', data=data)
    assert response.status_code < 400
 
def test_profinfo_get(client):
    response = client.get('/profinfo')
    assert response.status_code == 200
    assert b'Professor Information' in response.data

def test_profinfo_post(client):
    data = {
        'prof_name': 'Prof Test',
        'prof_email': 'prof@test.com',
        'prof_profile': 'http://test.com/prof',
        'prof_university': 'Test University'
    }
    response = client.post('/profinfo', data=data)
    assert response.status_code < 400

def test_profload_get(client):
    response = client.get('/profload')
    assert response.status_code == 200
    assert b'Download professor data' in response.data

def test_email_get(client):
    response = client.get('/email')
    assert response.status_code == 200
    assert b'Email' in response.data

def test_done_route(client):
    response = client.get('/done')
    assert response.status_code == 200
    assert b'Email sent' in response.data

def test_logout_route(client):
    response = client.get('/logout')
    assert response.status_code < 400

def test_clearprof_route(client):
    response = client.get('/clearprof')
    assert response.status_code < 400