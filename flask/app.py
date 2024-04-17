"""
Taken from another branch ahead of time to have classes available
"""
import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from stubs import *
from resources import OwnRecipes

api = Api(app)

@app.route("/")
def hello_world():
    user = db.session.execute(db.select(User))
    for r in user:
        print(r)
    return "<p>Hello, World!</p>"

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

api.add_resource(OwnRecipes, "/recipes/<username>")

if __name__ == '__main__':
    app.run(debug=True)
