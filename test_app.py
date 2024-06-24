import os
import pytest
from flask import Flask
from flask.testing import FlaskClient
from pymongo import MongoClient
from app import create_app

@pytest.fixture
def app():
    # Set up the Flask app for testing
    app = create_app()
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = os.getenv("MONGO_URI_TEST", "mongodb://root:root@mongo:27017/recommendations_db?authSource=admin")
    client = MongoClient(app.config['MONGO_URI'])
    db = client.get_database()
    with app.app_context():
        yield app
    

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

def test_index(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert b"itay's recommendation site" in response.data

def test_add_preference(client: FlaskClient):
    response = client.post('/add', data={
        'user_id': '1',
        'category': 'Music',
        'preference': 'Rock'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'1 - Music - Rock' in response.data

def test_generate_recommendations(client: FlaskClient):
    client.post('/add', data={
        'user_id': '2',
        'category': 'Books',
        'preference': 'Science Fiction'
    }, follow_redirects=True)
    response = client.get('/')
    assert b'2 - Science Fiction 1' in response.data


if __name__ == '__main__':
    pytest.main()