from flask import request, jsonify
from flask_restful import Resource, output_json
from webargs import fields
from webargs.flaskparser import use_kwargs
from sqlalchemy import update, text
from app_setup import *
from constants import *
from elastic import *

class GetRecipe(Resource):
    def get(self, recipe_id):

        recipe:Recipe = db.session.get(Recipe, recipe_id)
        if not recipe:
            return {"error":"recipe not in db"}, 404
        
        try:
            recipe_doc = get_document(recipe_id)
            recipe_doc[PICTURE] = recipe.picture

            return recipe_doc
        except:
            return {"error":"couldn't get recipe data"}, 404


class TrendingRecipe(Resource):
    def get(self):
        """
        Get a random/otherwise selected recipe and return it
        """

        """This returns some (random) recipe from elasticsearch"""
        return jsonify(get_random_document())


class SearchRecipes(Resource):
    
    @use_kwargs({QUERY: fields.String(required=True)}, location="query")
    def get(self, **kwargs):
        """
        Make an ES call for the search and return the results
        """        
        return search_data(kwargs[QUERY])


class FavoriteRecipes(Resource):

    def get(self, username):
        """
        get a list of the ids of a user's favorite recipes
        """
        user:User = db.session.get(User, username)

        res = []
        for r in user.favorites:
            id = r.recipe_id
            try:
                res.append(get_document(id))
            except:
                continue
        return res

    @use_kwargs({RECIPE_ID: fields.Integer(required=True)}, location="query")
    def put(self, username, **kwargs):
        """
        add a recipe to a user's favorites
        """
        if db.session.get(Favorite, kwargs[RECIPE_ID]):
            return 200
        
        fav:Favorite = Favorite(username=username, recipe_id=kwargs[RECIPE_ID])
        db.session.add(fav)
        db.session.commit()

        return 200

    @use_kwargs({RECIPE_ID: fields.Integer(required=True)}, location="query")
    def delete(self, username, **kwargs):
        """
        remove a recipe from a user's favorites
        """
        fav = db.session.get(Favorite, {USERNAME:username, RECIPE_ID:kwargs[RECIPE_ID]})
        db.session.delete(fav)
        db.session.commit()

        return 200


class OwnRecipes(Resource):

    def get(self, username):
        """
        get all ids of recipes created by user
        """
        user:User = db.session.get(User, username)

        results = []
        for r in user.recipes:
            id = r.recipe_id
            try:
                results.append(get_document(id))
            except:
                continue        
        return results

    def put(self, username):
        """
        create a recipe
        """
        json_data:dict = request.get_json(force=True)

        # if an id is passed, then the recipe must exist already
        if RECIPE_ID in json_data:
            if PICTURE in json_data:
                db.session.execute(
                    update(Recipe),
                    [
                        {
                            RECIPE_ID: json_data[RECIPE_ID],
                            PICTURE: json_data[PICTURE]
                        }
                    ]
                )
                db.session.commit()
                res = update_document(json_data[RECIPE_ID], json_data[RECIPE])
                return {"status": res}
        else:
            id = insert_document(json_data[RECIPE])

            picture = json_data.pop(PICTURE, None)
            recipe = Recipe(recipe_id=id, username=username, picture=picture)
            db.session.add(recipe)
            db.session.commit()

        return 200
    
    @use_kwargs({RECIPE_ID: fields.Integer(required=True)}, location="query")
    def delete(self, username, **kwargs):
        """
        delete a recipe
        """
        recipe = db.session.get(Recipe, kwargs[RECIPE_ID])
        if not recipe:
            return 200
        
        # if this fails, then the recipe id doesn't exist, which is the desired state
        try:
            delete_document(kwargs[RECIPE_ID])
        except:
            pass
        
        db.session.delete(recipe)
        db.session.commit()
        return 200


class RateRecipe(Resource):
    review_fields = {
        RECIPE_ID: fields.Integer(required=True),
        USERNAME: fields.String(required=True),
        RATING: fields.Boolean(required=False, default=True)
    }

    @use_kwargs({RECIPE_ID: fields.Integer(required=True)}, location="query")
    def get(self, **kwargs):
        """
        Get number of good recipe ratings
        """
        with db.engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) from review WHERE recipe_id = :id AND rating = 1"), 
                         {"id": kwargs[RECIPE_ID]}
                         ).scalar_one()
            return result

    @use_kwargs(review_fields, location="query")
    def put(self, **kwargs):
        """
        Give a rating to a recipe
        """
        review:Review = db.session.get(Review, {USERNAME:kwargs[USERNAME], RECIPE_ID:kwargs[RECIPE_ID]})
        if review:
            review.rating = kwargs[RATING]
        else:
            review = Review(username=kwargs[USERNAME], recipe_id=kwargs[RECIPE_ID], rating=kwargs[RECIPE_ID])
            db.session.add(review)

        db.session.commit()
        return 200


    @use_kwargs(review_fields, location="query")
    def delete(self, **kwargs):
        """
        Delete recipe rating
        """
        review = db.session.get(Review, {USERNAME:kwargs[USERNAME], RECIPE_ID:kwargs[RECIPE_ID]})
        if not review:
            return 200
        db.session.delete(review)
        db.session.commit()

        return 200
    
