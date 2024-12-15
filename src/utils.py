from models import StarWarsPlanet, db
import requests

def fetch_from_swapi(resource, id):
    url = f"https://swapi.py4e.com/api/{resource}/{id}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def extract_id_from_url(url):
    return int(url.rstrip("/").split("/")[-1])

def get_or_create_planet(data):
    # Extraer el ID del planeta desde la URL
    planet_id = extract_id_from_url(data["homeworld"])
    planet = db.session.get(StarWarsPlanet, planet_id)  # Uso del nuevo método de SQLAlchemy

    # Si el planeta no existe, solicitar datos de SWAPI y crearlo
    if not planet:
        planet_data = fetch_from_swapi("planets", planet_id)
        if not planet_data:  # Validar que SWAPI devolvió datos válidos
            raise ValueError(f"Planet with ID {planet_id} not found in SWAPI")

        planet = StarWarsPlanet(
            id=planet_id,
            name=planet_data.get("name", "Unknown"),
            climate=planet_data.get("climate", "unknown"),
            terrain=planet_data.get("terrain", "unknown"),
            population=planet_data.get("population", "unknown"),
        )
        db.session.add(planet)
        db.session.commit()

    return planet