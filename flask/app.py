"""
Taken from another branch ahead of time to have classes available
"""
import csv
from flask_restful import Api

from app_setup import *
from account_management import *
from resources import *
from elastic import *

api = Api(app)

default_creds = {"username": "", "password": ""}


@app.route("/")
def hello_world():
    user = db.session.execute(db.select(User))
    for r in user:
        print(r)
    return "<p>Hello, World!</p>"


@app.route("/drop")
def drop_es():
    drop_index()
    return "dropped es"


@app.route("/sanity")
def get_all_recipe():
    with db.engine.connect() as conn:
        r = conn.execute(text("SELECT * FROM recipe"))
        recipes = []
        for row in r:
            recipes.append(str(row))

        return recipes


@app.route("/init")
def init():
    with app.app_context():
        # Creates all the tables in the database
        try:
            db.drop_all()
            drop_es()
        except:
            pass
        db.create_all()

        # Check if the default user already exists
        existing_user = User.query.filter_by(username=default_creds["username"]).first()
        if existing_user is None:
            # Create the default user
            hashed_password = bcrypt.generate_password_hash(
                default_creds["password"]).decode('utf-8')
            new_user = User(username=default_creds["username"],
                            password=hashed_password,
                            is_admin=True)
            # Add the user to the database session
            db.session.add(new_user)
            db.session.commit()

    # Check if the Recipe table is empty
        if not Recipe.query.first():
            with open('RecipeNLG_dataset.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                # Skip header row
                next(reader)
                # Counter variable to keep track of rows read
                count = 0
                for row in reader:
                    # Break the loop if 10 rows have been read
                    if count >= 50:
                        break

                    doc = {
                        "title": row[1],
                        "ingredients": row[2],
                        "directions": row[3],
                        "description": "",
                        "keywords": []
                    }
                    id = insert_document(doc)
                    # The default username for pre-existing recipes is 'default', there are no associated pictures
                    recipe = Recipe(recipe_id=id,
                                    username=default_creds["username"],
                                    picture=None)
                    db.session.add(recipe)
                    count += 1
                db.session.commit()
    return "Done"


api.add_resource(GetRecipe, "/recipes/single/<recipe_id>")
api.add_resource(TrendingRecipe, "/recipes/trending")
api.add_resource(SearchRecipes, "/recipes/search")
api.add_resource(FavoriteRecipes, "/recipes/favorites/<username>")
api.add_resource(OwnRecipes, "/recipes/user/<username>")
api.add_resource(RateRecipe, "/recipes/rate")

if __name__ == '__main__':
    import sys
    default_creds["username"] = sys.argv[1]
    default_creds["password"] = sys.argv[2]
    app.run()
