from random import randint, choice as rc

from faker import Faker
from faker.providers import lorem

from app import app
from models import db, Movie, Actor, Credit


fake = Faker()
fake.add_provider(lorem)


genres = ["Action", "Comedy", "Drama", "Horror", "Romance", "Thriller", "Science Fiction",
          "Fantasy", "Mystery", "Adventure", "Crime", "Family", "Animation", "Documentary", "War"]

roles = ["Performer", "Director", "Producer", "Playwright",
         "Lighting Design", "Sound Design", "Set Design"]


def create_movies():
    movies = []
    for _ in range(25):
        m = Movie(
            rating=randint(1, 10),
            image="placeholder",
            genre=rc(genres),
            description=fake.paragraph(nb_sentences=5),
            title=fake.name()
        )
        movies.append(m)
    return movies


def create_actor():
    actors = []
    for _ in range(25):
        s = Actor(
            name=fake.name(),
            age=randint(11, 80),
        )
        actors.append(s)
    return actors


def create_credits(actors, movies):
    credits = []
    for _ in range(20):
        c = Credit(
            role=rc(roles),
            movie_id=rc(movies).id,
            actor_id=rc(actors).id
        )
        credits.append(c)
    return credits


if __name__ == '__main__':

    with app.app_context():

        print("Clearing db...")
        Credit.query.delete()
        Movie.query.delete()
        Actor.query.delete()

        print("Seeding Actors...")
        actors = create_actor()
        db.session.add_all(actors)
        db.session.commit()

        print("Seeding Movies...")
        movies = create_movies()
        db.session.add_all(movies)
        db.session.commit()

        print("Seeding Credits...")
        credits_list = create_credits(actors, movies)
        db.session.add_all(credits_list)
        db.session.commit()

        print("Done seeding!")
