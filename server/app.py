#!/usr/bin/env python3

from flask import Flask, request, session
from flask_restful import Resource, Api
from flask_migrate import Migrate
from models import db, User

# --------------------
# App Setup
# --------------------
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# REQUIRED for sessions
app.secret_key = "super-secret-key"

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# --------------------
# Resources
# --------------------

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")

        user = User.query.filter(User.username == username).first()

        if user:
            session["user_id"] = user.id
            return user.to_dict(), 200

        return {"error": "User not found"}, 401


class Logout(Resource):
    def delete(self):
        session.pop("user_id", None)
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")

        if user_id:
            user = User.query.get(user_id)
            return user.to_dict(), 200

        return {}, 401


class ClearSession(Resource):
    def get(self):
        session.pop("user_id", None)
        return {}, 204


# --------------------
# Route Registration
# --------------------
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")
api.add_resource(ClearSession, "/clear")

# --------------------
# Run App
# --------------------
if __name__ == "__main__":
    app.run(port=5555, debug=True)
