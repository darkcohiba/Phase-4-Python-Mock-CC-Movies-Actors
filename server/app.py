#!/usr/bin/env python3

from models import db, Movie, Actor, Credit
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)


class ActorResource(Resource):

    def get(self):
        actors_list = Actor.query.all()
        return [actor.to_dict() for actor in actors_list], 200

    def post(self):
        data = request.get_json()

        if not data:
            return {"message": "No input data provided"}, 400
        try:
            new_actor = Actor(name=data["name"], age=data['age'])
        except ValueError as e:
            return {"message": f"Error creating actor: {e}"}, 400

        db.session.add(new_actor)
        db.session.commit()

        return new_actor.to_dict(), 201


api.add_resource(ActorResource, '/actor')


class ActorsByIdResource(Resource):

    def get(self, actor_id):
        if actor := Actor.query.get(actor_id):
            return actor.to_dict(), 200
        else:
            return {"message": "Actor not found"}, 404

    def patch(self, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            return {"message": "Actor not found"}, 404

        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400

        allowed_fields = {"name", "age"}
        try:
            for field in data:
                if field in allowed_fields:
                    setattr(actor, field, data[field])
                else:
                    return {"message": f"Field '{field}' is not allowed to be updated"}, 400
        except ValueError as e:
            return {"message": f"Error updating field '{field}': {e}"}, 400

        db.session.commit()

        return actor.to_dict(), 202

    def delete(self, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            return {"message": "Actor not found"}, 404

        db.session.delete(actor)
        db.session.commit()

        return {}, 204


api.add_resource(ActorsByIdResource, '/actor/<int:actor_id>')


class MovieResource(Resource):

    def get(self):
        movies_list = Movie.query.all()
        return [movie.to_dict() for movie in movies_list], 200

    def post(self):
        data = request.get_json()

        if not data:
            return {"message": "No input data provided"}, 400
        try:
            new_movie = Movie(
                rating=data['rating'],
                image=data['image'],
                genre=data['genre'],
                description=data['description'],
                title=data['title']
            )
        except ValueError as e:
            return {"message": f"Error creating movie: {e}"}, 400

        db.session.add(new_movie)
        db.session.commit()

        return new_movie.to_dict(), 201


api.add_resource(MovieResource, '/movie')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
