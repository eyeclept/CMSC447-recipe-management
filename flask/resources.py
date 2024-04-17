from flask import request, jsonify
from flask_restful import Resource
import sqlalchemy
from webargs import fields
from webargs.flaskparser import use_kwargs
from sqlalchemy import update
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
        user:User = db.session.get(User, username)

        ids = []
        for r in user.recipes:
            ids.append(r.recipe_id)

        return stubbed_elasticsearch_call(ids)


    def post(self, username):
        """
        create a recipe
        """
        json_data = request.get_json(force=True)
        id = json_data['recipe_id']
        picture = None
        if 'picture' in json_data:
            picture = json_data['picture']
        
        recipe = Recipe(recipe_id=id, username=username, picture=picture)
        db.session.add(recipe)
        db.session.commit()

        es = stubbed_elasticsearch_call(json_data)
        es['id'] = id
        return es


    def put(self, username):
        """
        create a recipe
        """
        json_data = request.get_json(force=True)
        id = json_data['recipe_id']
        
        if 'picture' in json_data:
            db.session.execute(
                update(Recipe),
                [
                    {
                        'recipe_id': id,
                        'picture': json_data['picture']
                    }
                ]
            )
            db.session.commit()

        es = stubbed_elasticsearch_call(json_data)
        es['id'] = id
        return es
    
    @use_kwargs({'recipe_id': fields.Integer()}, location="query")
    def delete(self, username, **kwargs):
        """
        delete a recipe
        """
        es = stubbed_elasticsearch_call(kwargs)

        recipe = db.session.get(Recipe, kwargs['recipe_id'])
        db.session.delete(recipe)
        db.session.commit()
        return es

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
    