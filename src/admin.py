from flask import Blueprint
from models import db

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/reset-db", methods=["POST"])
def reset_db():
    db.drop_all()
    db.create_all()
    return {"message": "Database reset successfully"}


@admin_bp.route("/admin/load-sample-data", methods=["POST"])
def load_sample_data():
    from models import StarWarsFilm, StarWarsPerson
    sample_film = StarWarsFilm(
        title="A New Hope",
        director="George Lucas",
        release_date="1977-05-25",
        episode_id=4,
        opening_crawl="It is a period of civil war..."
    )
    sample_person = StarWarsPerson(
        name="Luke Skywalker",
        gender="Male",
        birth_year="19BBY"
    )
    db.session.add_all([sample_film, sample_person])
    db.session.commit()
    return {"message": "Sample data loaded successfully"}