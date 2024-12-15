from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo para Películas
class StarWarsFilm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.String(20), nullable=False)
    episode_id = db.Column(db.Integer, nullable=True)
    opening_crawl = db.Column(db.Text, nullable=True)

# Modelo para Personas
class StarWarsPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(50), nullable=True)
    height = db.Column(db.String(20), nullable=True)
    birth_year = db.Column(db.String(20), nullable=True)
    homeworld = db.Column(db.String(50), nullable=True)
    

# Modelo para Planetas
class StarWarsPlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    diameter = db.Column(db.String(10), nullable=True)
    gravity = db.Column(db.String(10), nullable=True)
    climate = db.Column(db.String(50), nullable=True)
    terrain = db.Column(db.String(100), nullable=True)
    population = db.Column(db.String(50), nullable=True)

# Modelo para Especies
class StarWarsSpecies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    classification = db.Column(db.String(50), nullable=True)
    language = db.Column(db.String(50), nullable=True)
    average_height = db.Column(db.String(20), nullable=True)
    average_lifespan = db.Column(db.String(20), nullable=True)

# Modelo para Starships
class StarWarsStarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=True)
    starship_class = db.Column(db.String(50), nullable=True)
    max_atmosphering_speed = db.Column(db.String(50), nullable=True)
    manufacturer = db.Column(db.String(100), nullable=True)
    cost_in_credits = db.Column(db.String(50), nullable=True)

# Modelo para Vehículos
class StarWarsVehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=True)
    vehicle_class = db.Column(db.String(50), nullable=True)
    max_atmosphering_speed = db.Column(db.String(50), nullable=True)
    manufacturer = db.Column(db.String(100), nullable=True)
    cost_in_credits = db.Column(db.String(50), nullable=True)