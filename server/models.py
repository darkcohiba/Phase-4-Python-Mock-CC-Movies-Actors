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





class Actor(db.Model, SerializerMixin):
    __tablename__ = 'actor_table'

    id = db.Column(db.Integer, primary_key=True)



class Credit(db.Model, SerializerMixin):
    __tablename__ = 'credit_table'
