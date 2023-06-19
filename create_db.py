from app import db, app, Film
import json

def create_db():
    with open('films.json', 'r') as data:
        films = json.load(data)

        for film in films:
            new_film = Film(
                films[film]['brand'],
                film,
                films[film]['film_type'],
                films[film]['formats'],
                films[film]['origin'],
                films[film]['process'],
                films[film]['film_speed'],
                films[film]['grain'],
                films[film]['contrast'],
                films[film]['facts']
            )
            db.session.add(new_film)
            db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_db()