from flask_jwt_extended import create_access_token, jwt_required
from flask import request, jsonify

from app_setup import *


# Registering as a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Expecting JSON data from React frontend
    given_username = data.get('username')
    given_password = data.get('password')

    # Input validation
    if not given_username or not given_password:
        return jsonify({'message': 'Please enter a username and password.'
                       }), 400

    # Check if username already exists
    existing_user = User.query.filter_by(username=given_username).first()
    if existing_user:
        return jsonify({
            'message': 'Username already exists, please enter a different one.'
        }), 400

    try:
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(given_password).decode(
            'utf-8')

        # Create the new user
        new_user = User(username=given_username,
                        password=hashed_password,
                        is_admin=False)

        # Add the user to the database session
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully.'}), 201
    except Exception as e:
        # Rollback changes if an exception occurs
        db.session.rollback()
        return jsonify({'message': f'Error registering user: {str(e)}'}), 500


# Logging in
# React frontend will have to check if a token doesn't exist in local storage before calling this
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Expecting JSON data from React frontend
    given_username = data.get('username')
    given_password = data.get('password')

    # Query the database to find the user by username
    user = User.query.filter_by(username=given_username).first()

    # If the password associated with the username in the db matches the given password
    if user and bcrypt.check_password_hash(user.password, given_password):
        access_token = create_access_token(identity=user.username)
        return jsonify({'access_token': access_token
                       }), 200  # React wil need to store this
    else:
        return jsonify({'message': 'Invalid username or password.'}), 401


# Logging Out
# React frontend needs to check if a token exists
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # For JWT, logging out is handled on the client side by deleting the token.
    return jsonify({'message': 'Logged out successfully.'}), 200


""" 
Below is an example of using a JWT to get the logged in user's recipes from the recipe db
React frontend will have to check if a token doesn't exist in local storage before calling this
React frontend will have to check if the token isn't expired before calling this
If the token is expired, react needs to delete the token and then redirect to login
@app.route('/recipes/user', methods=['GET'])
@jwt_required()
def get_user_recipes():
    current_user = get_jwt_identity()
    recipes = Recipe.query.filter_by(username=current_user).all()
    recipes_list = [{'recipe_id': recipe.recipe_id, 'picture': recipe.picture} for recipe in recipes]
    return jsonify({'recipes': recipes_list}), 200
"""
