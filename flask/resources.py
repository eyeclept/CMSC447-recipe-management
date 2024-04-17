from flask import request, jsonify
from flask_restful import Resource
import sqlalchemy
from webargs import fields
from webargs.flaskparser import use_kwargs

from stubs import *

class SearchRecipes(Resource):
    
    def get(self):
        """
        Make an ES call for the search and return the results

        query terms passed as json? not sure, need to talk to front end
        """
        return stubbed_elasticsearch_call()


class FavoriteRecipes(Resource):

    def get(self, username):
        """
        get a list of the ids of a user's favorite recipes
        """
        pass


    
    def post(self, username):
        """
        add a recipe to a user's favorites
        """
        pass

    def delete(self, username):
        """
        remove a recipe from a user's favorites
        """
        pass


class OwnRecipes(Resource):

    def get(self, username):
        """
        get all ids of recipes created by user
        """
        user:User = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()
        
        for r in user.recipes:
            print(r)

        return "abcd"

    def put(self, username):
        """
        update/create a recipe
        """
        pass

    def delete(self, username):
        """
        delete a recipe
        """
        pass


class RateRecipe(Resource):

    def get(self, username):
        """
        get avg/total rating for a recipe (dunno how we're doing it)
        """
        pass

    def put(self, username):
        """
        give a rating to a recipe
        """
        pass

    def delete(self, username):
        """
        delete recipe rating
        """
        pass
    