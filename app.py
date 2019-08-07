from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://jbpasptyyqgbmb:11766f515866a1d35b514eeeb2632aa13638f6058f530152db21936df7031398@ec2-174-129-209-212.compute-1.amazonaws.com:5432/dbd234jka4s3ro"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Snack(db.Model):
    __tablename__ = "snacks"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    image = db.Column(db.String(800))
    price = db.Column(db.Float)
    favorite = db.Column(db.Boolean)

    def __init__(self, text, image, price, favorite):
        self.text = text
        self.image = image
        self.price = price
        self.favorite = favorite


class SnackSchema(ma.Schema):
    class Meta:
        fields = ("id", "text", "image", "price", "favorite")


snack_schema = SnackSchema()
snacks_schema = SnackSchema(many=True)


@app.route("/")
def greeting():
    return "<h1>Hello</h1>"


@app.route("/snacks", methods=["GET"])
def get_snacks():
    all_snacks = Snack.query.all()
    result = snacks_schema.dump(all_snacks)
    return jsonify(result.data)


@app.route("/snack/<id>", methods=["GET"])
def get_snack(id):
    snack = Snack.query.get(id)
    return snack_schema.jsonify(snack)


@app.route("/add-snack", methods=["POST"])
def add_snack():
    text = request.json["text"]
    image = request.json["image"]
    price = request.json["price"]
    favorite = request.json["favorite"]

    new_snack = Snack(text, image, price, favorite)

    db.session.add(new_snack)
    db.session.commit()

    return jsonify("ADDED!")


@app.route("/snack/<id>", methods=["DELETE"])
def delete_snack(id):
    snack = Snack.query.get(id)
    db.session.delete(snack)
    db.session.commit()

    return jsonify("DELETED")


@app.route("/snack/<id>", methods=["PUT"])
def update_snack(id):
    snack = Snack.query.get(id)

    new_text = request.json["text"]
    new_image = request.json["image"]
    new_price = request.json["price"]
    new_favorite = request.json["favorite"]

    snack.text = new_text
    snack.image = new_image
    snack.price = new_price
    snack.favorite = new_favorite

    db.session.commit()
    return snack_schema.jsonify(snack)


if __name__ == "__main__":
    app.run(debug=True)
