import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import random

app = Flask(__name__)
# Replace with the actual url to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
FAKE_ES = {}


class User(db.Model):
    username = db.Column(db.String(255), primary_key=True, nullable=False)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean)
    recipes = db.relationship('Recipe', backref='user')
    reviews = db.relationship('Review', backref='user')
    favorites = db.relationship('Favorite', backref='user')

class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(255), db.ForeignKey('user.username'))
    picture = db.Column(db.LargeBinary)
    reviews_1 = db.relationship('Review', backref='recipe')
    favorites_1 = db.relationship('Favorite', backref='recipe')

class Review(db.Model):
    username = db.Column(db.String(255), db.ForeignKey('user.username'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), primary_key=True)
    rating = db.Column(db.Boolean)

class Favorite(db.Model):
    username = db.Column(db.String(255), db.ForeignKey('user.username'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), primary_key=True)


def stubbed_elasticsearch_call(*args, **kwargs):
    """
    For now, placeholder function for ES
    """
    
    if 'recipe_id' in kwargs:
        return FAKE_ES[kwargs['recipe_id']]
    if all([isinstance(x, int) for x in args]):
        return {x:FAKE_ES[x] for x in args}
    return FAKE_ES
