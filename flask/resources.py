from flask import request, jsonify
from flask_restful import Resource
import sqlalchemy
from webargs import fields
from webargs.flaskparser import use_kwargs

from stub_fillers import *


class SearchRecipes(Resource):
    
    def get(self):
        """
        Make an ES call for the search and return the results
        """
        return stubbed_elasticsearch_call()


class FavoriteRecipes(Resource):

    def get(self):
        """
        get a list of the ids of a user's favorite recipes
        """
        pass
    
    def post(self):
        """
        add a recipe to a user's favorites
        """
        pass

    def delete(self):
        """
        remove a recipe from a user's favorites
        """
        pass


class OwnRecipes(Resource):

    def get(self):
        """
        get all ids of recipes created by user
        """
        pass

    def put(self):
        """
        update/create a recipe
        """
        pass

    def delete(self):
        """
        delete a recipe
        """
        pass


class RateRecipe(Resource):

    def get(self):
        """
        get avg/total rating for a recipe (dunno how we're doing it)
        """
        pass

    def put(self):
        """
        give a rating to a recipe
        """
        pass

    def delete(self):
        """
        delete recipe rating
        """
        pass