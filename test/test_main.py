import pytest
from src.main import app, db
from unittest.mock import patch
from src.utils import fetch_from_swapi

@pytest.fixture
def client():
    """Fixture para configurar el cliente de pruebas."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

# ----- PRUEBAS DEL ENDPOINT RAÍZ -----
def test_root_endpoint(client):
    """Prueba del endpoint raíz '/'."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"The app is up!"

# ----- PRUEBAS DE LOS ENDPOINTS SWAPI -----
@patch('src.main.requests.get')
def test_get_swapi_resource(mock_get, client):
    """Prueba del endpoint /swapi/<resource>."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"count": 10}

    response = client.get("/swapi/people")
    assert response.status_code == 200
    assert response.json["count"] == 10

def test_get_swapi_resource_not_found(client):
    """Prueba de recurso no encontrado en /swapi/<resource>."""
    response = client.get("/swapi/invalid_resource")
    assert response.status_code == 404

@patch('src.main.requests.get')
def test_search_swapi_resource(mock_get, client):
    """Prueba del endpoint /swapi/<resource>/search."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"results": [{"name": "Luke Skywalker"}]}

    response = client.get("/swapi/people/search?search=Luke")
    assert response.status_code == 200
    assert response.json["results"][0]["name"] == "Luke Skywalker"

@patch('src.main.requests.get')
def test_get_resource_by_id(mock_get, client):
    """Prueba del endpoint /swapi/<resource>/<id>."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"name": "Luke Skywalker"}

    response = client.get("/swapi/people/1")
    assert response.status_code == 200
    assert response.json["name"] == "Luke Skywalker"

# ----- PRUEBA DEL ENDPOINT SAVE RESOURCE -----
@patch('src.utils.fetch_from_swapi')
def test_save_resource(mock_fetch, client):
    """Prueba del endpoint /<resource>/save/<id>."""
    mock_fetch.return_value = {
        "name": "Luke Skywalker",
        "gender": "male",
        "height": "172",
        "birth_year": "19BBY",
        "homeworld": "https://swapi.py4e.com/api/planets/1/"
    }
    response = client.post("/people/save/1")
    assert response.status_code == 201
    assert b"Luke Skywalker saved successfully" in response.data

def test_save_resource_invalid(client):
    """Prueba de recurso inválido en /<resource>/save/<id>."""
    response = client.post("/invalid/save/1")
    assert response.status_code == 400

# ----- PRUEBA DEL ENDPOINT LOCAL RESOURCE -----
def test_get_local_resources_empty(client):
    """Prueba del endpoint /<resource>/local cuando no hay datos."""
    response = client.get("/people/local")
    assert response.status_code == 200
    assert response.json == []

def test_get_local_resources_invalid(client):
    """Prueba de recurso inválido en /<resource>/local."""
    response = client.get("/invalid/local")
    assert response.status_code == 400

# ----- PRUEBAS DE LOS ENDPOINTS ADMIN -----
def test_reset_db(client):
    """Prueba del endpoint /admin/reset-db."""
    response = client.post("/admin/reset-db")
    assert response.status_code == 200
    assert response.json["message"] == "Database reset successfully"