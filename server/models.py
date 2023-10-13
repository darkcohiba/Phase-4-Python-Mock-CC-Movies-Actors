from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Movie(db.Model, SerializerMixin):
    __tablename__ = 'movie_table'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    image = db.Column(db.String)
    description = db.Column(db.String)
    rating = db.Column(db.Integer)

    # relationship to credits
    movie_credits = db.relationship('Credit', back_populates='related_movie', cascade="all, delete-orphan")

    @validates('rating')
    def validate_rating(self, key, rating):
        if 0 < rating < 11 and isinstance(rating, int):
            return rating
        else:
            raise ValueError("Rating must be between 1 and 10")

    @validates('genre')
    def validate_genre(self, key, genre):
        genres = ["Action", "Comedy", "Drama", "Horror", "Romance", "Thriller", "Science Fiction",
                  "Fantasy", "Mystery", "Adventure", "Crime", "Family", "Animation", "Documentary", "War"]
        # display my genres as a bullet point list
        genres_str = "\n- " + "\n- ".join(genres)
        if genre not in genres:
            raise ValueError(f"Genre must be one of: {genres_str}")
        return genre


class Actor(db.Model, SerializerMixin):
    __tablename__ = 'actor_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    # relationship to credits
    actor_credits = db.relationship('Credit', back_populates='related_actor', cascade="all, delete-orphan")

    # validations

    @validates('age')
    def validate_age(self, key, age):
        if age < 11 and isinstance(age, int):
            raise ValueError("Must be older than 10.")
        return age


class Credit(db.Model, SerializerMixin):
    __tablename__ = 'credit_table'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)
    # foreign key for movies
    movie_id = db.Column(db.Integer, db.ForeignKey(
        'movie_table.id'), nullable=False)
    # relationship for movies
    related_movie = db.relationship('Movie', back_populates='movie_credits')

    # foreign key for actors
    actor_id = db.Column(db.Integer, db.ForeignKey(
        'actor_table.id'), nullable=False)
    # relationship for actors
    related_actor = db.relationship('Actor', back_populates='actor_credits')

    @validates('role')
    def validate_role(self, key, role):
        roles = ["Performer", "Director", "Producer", "Playwright",
                 "Lighting Design", "Sound Design", "Set Design"]
        # display my roles as a bullet point list
        roles_str = "\n- " + "\n- ".join(roles)
        if role not in roles:
            raise ValueError(f"Role must be a qualifed role: {roles_str}")
        return role

    serialize_rules=('-related_actor.actor_credits', '-related_movie.movie_credits')