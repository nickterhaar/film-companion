from app import db, app, hash, Film, User
import json

def admin_user():
    first_name = 'Film'
    last_name = 'Companion'
    username = 'admin'
    email = 'admin@filmcompanion.com'
    password = 'admin123'
    pass_hash = hash.hash_value(password, salt=username)
    admin = True

    new_admin = User(first_name, last_name, username, email, pass_hash, admin)
    db.session.add(new_admin)
    db.session.commit()

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
                films[film]['facts'],
                films[film]['image']
            )
            db.session.add(new_film)
            db.session.commit()
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_db()
        admin_user()