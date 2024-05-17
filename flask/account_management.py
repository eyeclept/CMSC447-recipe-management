from flask_login import login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Registering as a new user
@app.route('/register', methods=['POST'])
def register():
    given_username = request.form['username']
    given_password = request.form['password']

    # Input validation
    if not given_username or not given_password:       
        return 'Please enter a username and password.'

    # Check if username already exists
    existing_user = User.query.filter_by(username=given_username).first()
    if existing_user:
        return 'Username already exists, please enter a different one.'

    try:
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(given_password).decode('utf-8')

        # Create the new user
        new_user = User(username=given_username, password=hashed_password, is_admin=False)

        # Add the user to the database session
        db.session.add(new_user)
        db.session.commit()

        return 'User registered successfully.'
    except Exception as e:
        # Rollback changes if an exception occurs
        db.session.rollback()
        return f'Error registering user: {str(e)}'


# Logging in
@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return "User already logged in."

    given_username = request.form['username']
    given_password = request.form['password']

    # Query the database to find the user by username
    user = User.query.filter_by(username=given_username).first()
    if user and bcrypt.check_password_hash(user.password, given_password):
        login_user(user)
        return 'Login successful.'
    else:
        return 'Invalid username or password.'

#Logging Out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully.'
