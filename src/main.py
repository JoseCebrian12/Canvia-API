from flask import Flask, jsonify, request
from models import StarWarsStarship, StarWarsFilm, StarWarsPerson, StarWarsSpecies, StarWarsPlanet, StarWarsVehicle, db
import requests
from admin import admin_bp
from utils import fetch_from_swapi, get_or_create_planet

app = Flask(__name__)
app.register_blueprint(admin_bp)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///starwars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Crear las tablas
with app.app_context():
    db.create_all()

# ----- ENDPOINTS GENERALES -----
@app.route("/swapi/<resource>", methods=["GET"])
def get_swapi_resource(resource):
    url = f"https://swapi.py4e.com/api/{resource}/"
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())
    return {"error": f"Resource {resource} not found"}, 404

@app.route("/swapi/<resource>/search", methods=["GET"])
def search_swapi_resource(resource):
    query = request.args.get("search", "")
    url = f"https://swapi.py4e.com/api/{resource}/?search={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())
    return {"error": f"No results found for '{query}' in {resource}"}, 404

@app.route("/swapi/<resource>/<int:id>", methods=["GET"])
def get_resource_by_id(resource, id):
    url = f"https://swapi.py4e.com/api/{resource}/{id}/"
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())
    return {"error": f"Resource '{resource}' with ID {id} not found"}, 404

# ----- RECURSOS SWAPI -----
RESOURCE_MAPPING = {
    "films": (StarWarsFilm, {"title", "director", "release_date", "episode_id", "opening_crawl"}),
    "people": (StarWarsPerson, {"name", "gender", "height", "birth_year", "homeworld"}),
    "planets": (StarWarsPlanet, {"name", "diameter", "gravity", "climate", "terrain", "population"}),
    "species": (StarWarsSpecies, {"name", "classification", "language", "average_height", "average_lifespan"}),
    "starships": (StarWarsStarship, {"name", "model", "starship_class", "max_atmosphering_speed", "manufacturer", "cost_in_credits"}),
    "vehicles": (StarWarsVehicle, {"name", "model", "vehicle_class","max_atmosphering_speed", "manufacturer", "cost_in_credits"}),
}

@app.route("/<resource>/save/<int:id>", methods=["POST"])
def save_resource(resource, id):
    if resource not in RESOURCE_MAPPING:
        return {"error": "Invalid resource type"}, 400

    model, fields = RESOURCE_MAPPING[resource]
    data = fetch_from_swapi(resource, id)

    if data:
        resource_data = {field: data.get(field) for field in fields}

        # Manejo especial para el campo 'homeworld' en 'people'
        if resource == "people" and "homeworld" in data:
            planet = get_or_create_planet(data)
            resource_data["homeworld"] = planet.name  # Almacena el nombre del planeta en lugar del objeto completo

        new_entry = model(**resource_data)
        db.session.add(new_entry)
        db.session.commit()

        return {"message": f"{data['name'] if 'name' in data else data['title']} saved successfully"}, 201
    return {"error": f"{resource} not found"}, 404

@app.route("/<resource>/local", methods=["GET"])
def get_local_resources(resource):
    if resource not in RESOURCE_MAPPING:
        return {"error": "Invalid resource type"}, 400

    model, fields = RESOURCE_MAPPING[resource]
    entries = model.query.all()
    result = [{field: getattr(entry, field) for field in fields} for entry in entries]
    return jsonify(result)

# ----- ROOT -----
@app.route("/")
def get_feature():  
    return "The app is up!"

if __name__ == '__main__':
    app.run(debug=True)
