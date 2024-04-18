import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Replace with the actual url to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///replace_me.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(255), db.ForeignKey('user.username'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'))
    rating = db.Column(db.Boolean)

class Favorite(db.Model):
    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(255), db.ForeignKey('user.username'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'))

with app.app_context():
    # Creates all the tables in the database
    db.create_all()

    # Create a new user
    new_user = User(username='default', password='default', is_admin=False)   
    # Add the user to the database session
    db.session.add(new_user)  
    db.session.commit()

    # Read the first 10 rows of the pre-existing recipes from RecipeNLG_dataset.csv and insert into recipe table
    with open('RecipeNLG_dataset.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        # Skip header row
        next(reader)  
        # Counter variable to keep track of rows read
        count = 0
        for row in reader:
            # Break the loop if 10 rows have been read
            if count >= 10:
                break
            # The first column contains the recipe IDs
            id = int(row[0])
            # The default username for pre-existing recipes is 'default', there are no associated pictures
            recipe = Recipe(recipe_id=id, username='default', picture=None)
            db.session.add(recipe)
            count += 1
    db.session.commit()