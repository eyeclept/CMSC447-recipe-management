from flask_login import login_user, logout_user, current_user, login_required
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Registering as a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        given_username = request.form['username']
        given_password = request.form['password']

        # Input validation
        if not given_username or not given_password:
            return 'Please enter a username and password.'

        # Check if username already exists
        existing_user = User.query.filter_by(username=given_username).first()
        if existing_user:
            return 'Username already exists, please enter a different one.'

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(given_password).decode('utf-8')

        # Create the new user
        new_user = User(username=given_username, password=hashed_password, is_admin=False)

        # Add the user to the database session
        db.session.add(new_user)
        db.session.commit()

        return 'User registered successfully.'

    # This part only runs if the request was a get
    return render_template('register.html') # Replace with actual html name

# Logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return "User already logged in."

    if request.method == 'POST':
        given_username = request.form['username']
        given_password = request.form['password']

        # Query the database to find the user by username
        user = User.query.filter_by(username=given_username).first()
        if user and bcrypt.check_password_hash(user.password, given_password):
            login_user(user)
            return 'Login successful.'
        else:
            return 'Invalid username or password.'

    # This part only runs if the request was a get
    return render_template('login.html')   # Replace with actual html name

#Logging Out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully.'
