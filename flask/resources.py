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
        user:User = db.session.get(User, username)

        ids = []
        for r in user.favorites:
            ids.append(r.recipe_id)

        return stubbed_elasticsearch_call(ids)

    @use_kwargs({"recipe_id": fields.Integer(required=True)}, location="query")
    def put(self, username, **kwargs):
        """
        add a recipe to a user's favorites
        """
        if db.session.get(Favorite, kwargs['recipe_id']):
            return 200
        
        fav:Favorite = Favorite(username=username, recipe_id=kwargs['recipe_id'])
        db.session.add(fav)
        db.session.commit()

        return 200

    @use_kwargs({"recipe_id": fields.Integer(required=True)}, location="query")
    def delete(self, username, **kwargs):
        """
        remove a recipe from a user's favorites
        """
        fav = db.session.get(Favorite, {'username':username, 'recipe_id':kwargs['recipe_id']})
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

        return stubbed_elasticsearch_call(ids)

    def put(self, username):
        """
        create a recipe
        """
        json_data:dict = request.get_json(force=True)

        # if an id is passed, then the recipe must exist already
        if id in json_data:
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
        else:
            # have to get the id from elasticsearch
            es = stubbed_elasticsearch_call(json_data)
            id = es['id']
            picture = json_data.pop('picture', None)
            recipe = Recipe(recipe_id=id, username=username, picture=picture)
            db.session.add(recipe)
            db.session.commit()


        return "done"
    
    @use_kwargs({'recipe_id': fields.Integer(required=True)}, location="query")
    def delete(self, username, **kwargs):
        """
        delete a recipe
        """
        recipe = db.session.get(Recipe, kwargs['recipe_id'])
        if not recipe:
            return 200
        es = stubbed_elasticsearch_call(kwargs)

        db.session.delete(recipe)
        db.session.commit()
        return es

class RateRecipe(Resource):
    review_fields = {
        'recipe_id': fields.Integer(required=True),
        'username': fields.String(required=True),
        'rating': fields.Boolean(required=False, default=True)
    }

    @use_kwargs({'recipe_id': fields.Integer(required=True)}, location="query")
    def get(self, **kwargs):
        """
        get avg/total rating for a recipe (dunno how we're doing it)
        """
        pass

    @use_kwargs(review_fields, location="query")
    def put(self, **kwargs):
        """
        give a rating to a recipe
        """
        review:Review = db.session.get(Review, {'username':kwargs['username'], 'recipe_id':kwargs['recipe_id']})
        if review:
            review.rating = kwargs['rating']
        else:
            review = Review(username=kwargs['username'], recipe_id=kwargs['recipe_id'], rating=kwargs['rating'])
            db.session.add(review)

        db.session.commit()
        return 200


    @use_kwargs(review_fields, location="query")
    def delete(self, **kwargs):
        """
        delete recipe rating
        """
        review = db.session.get(Review, {'username':kwargs['username'], 'recipe_id':kwargs['recipe_id']})
        if not review:
            return 200
        db.session.delete(review)
        db.session.commit()

        return 200
    