from flask import request, jsonify
from flask_restful import Resource
import sqlalchemy
from webargs import fields
from webargs.flaskparser import use_kwargs
from sqlalchemy import update, text
from app_setup import *
from constants import *

class GetRecipe(Resource):
    def get(self, recipe_id):

        recipe:Recipe = db.session.get(Recipe, recipe_id)
        if not recipe:
            return 404
        
        """This should return the document in elastic search with the given ID"""
        recipe_doc = stubbed_elasticsearch_call(recipe_id)
        recipe_doc[PICTURE] = recipe.picture

        return recipe_doc


class TrendingRecipe(Resource):
    def get(self):
        """
        Get a random/otherwise selected recipe and return it
        """

        """This returns some (random) recipe from elasticsearch"""
        return stubbed_elasticsearch_call()


class SearchRecipes(Resource):
    
    @use_kwargs({QUERY: fields.String()}, location="query")
    def get(self, **kwargs):
        """
        Make an ES call for the search and return the results
        """        
        return stubbed_elasticsearch_call(kwargs["query"])


class FavoriteRecipes(Resource):

    def get(self, username):
        """
        get a list of the ids of a user's favorite recipes
        """
        user:User = db.session.get(User, username)

        ids = []
        for r in user.favorites:
            ids.append(r.recipe_id)

        """This should return all recipes with id's in the passed list"""
        return stubbed_elasticsearch_call(*ids)

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

        ids = []
        for r in user.recipes:
            ids.append(r.recipe_id)
        
        """This can be the exact same call as in the get for FavoriteRecipes"""
        return stubbed_elasticsearch_call(*ids)

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

        else:
            # have to get the id from elasticsearch, not this placeholder
            """ The actual order of operations should be insert into Elastic-
                Search FIRST, then get the id from the newly inserted field,
                and then add it to the database.
            """
            id = random.randint(100,1000)
            FAKE_ES[id] = json_data[RECIPE]

            picture = json_data.pop(PICTURE, None)
            recipe = Recipe(recipe_id=id, username=username, picture=picture)
            db.session.add(recipe)
            db.session.commit()

        return "done"
    
    @use_kwargs({RECIPE_ID: fields.Integer(required=True)}, location="query")
    def delete(self, username, **kwargs):
        """
        delete a recipe
        """
        recipe = db.session.get(Recipe, kwargs[RECIPE_ID])
        if not recipe:
            return 200
        """Delete from ElasticSearch where recipe_id matches"""
        es = stubbed_elasticsearch_call(**kwargs)

        db.session.delete(recipe)
        db.session.commit()
        return es


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
    
