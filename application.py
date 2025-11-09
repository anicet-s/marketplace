from datetime import timedelta

from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
import os
import json
import requests
from authlib.integrations.flask_client import OAuth
import logging
from sqlalchemy.dialects.postgresql import BIGINT

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

application = Flask(__name__)
application.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# Database configuration
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/catalogmenuwithusers'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
application.config['SESSION_PERMANENT'] = True

db = SQLAlchemy(application)

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Configure OAuth with Authlib
oauth = OAuth(application)
google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
    server_metadata_url=GOOGLE_DISCOVERY_URL,
)


# User model
class User(UserMixin, db.Model):
    id = db.Column(BIGINT, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))


# Item model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    category = db.Column(db.String(50))
    icon_url = db.Column(db.String(500), nullable=True)
    specifications = db.Column(db.JSON, nullable=True)


# Login manager
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Routes
@application.route('/')
def index():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return render_template('home.html')
    return render_template('login.html')


@application.route('/furniture')
@login_required
def furniture():
    items = Item.query.filter_by(category='furniture').all()
    return render_template('furniture.html', items=items)


@application.route('/login')
def login():
    # Initialize OAuth flow with Google
    # Generate secure nonce for CSRF protection
    nonce = os.urandom(16).hex()
    session['nonce'] = nonce
    logging.debug(f"Generated nonce and stored in session: {nonce}")
    # Redirect to Google's authentication page
    return oauth.google.authorize_redirect(redirect_uri=url_for('auth', _external=True), nonce=nonce)


@application.route('/auth')
def auth():
    try:
        # Exchange authorization code for access token
        token = oauth.google.authorize_access_token()
        logging.debug("Successfully exchanged authorization code for access token")
    except Exception as e:
        logging.error(f"Failed to exchange authorization code for token: {str(e)}")
        return redirect(url_for('login'))
    
    try:
        # Retrieve user information from Google
        user_info = google.get('userinfo').json()
        session['user_info'] = user_info
        logging.debug(f"Retrieved user info: {user_info.get('email')}")
    except Exception as e:
        logging.error(f"Failed to retrieve user info from Google: {str(e)}")
        return redirect(url_for('login'))
    
    try:
        # Extract user details
        id = user_info['id']
        email = user_info['email']
        name = user_info['name']

        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()
        if not user:
            # Create a new user if not found
            user = User(id=int(id), email=email, name=name)
            db.session.add(user)
            db.session.commit()
            logging.info(f"Created new user: {email}")
        else:
            logging.debug(f"Existing user logged in: {email}")
        
        # Log the user in
        login_user(user)
        session.permanent = True
        return redirect('/')
    except Exception as e:
        logging.error(f"Database error during user creation/login: {str(e)}")
        db.session.rollback()
        return redirect(url_for('login'))


@application.route('/logout')
@login_required
def logout():
    # Log out the user using Flask-Login
    logout_user()
    # Clear any additional session data
    session.clear()
    logging.info("User logged out successfully")
    return redirect(url_for('login'))


@application.route('/cars')
@login_required
def cars():
    items = Item.query.filter_by(category='cars').all()
    return render_template('cars.html', items=items)


@application.route('/houses')
@login_required
def houses():
    items = Item.query.filter_by(category='houses').all()
    return render_template('houses.html', items=items)


if __name__ == '__main__':
    application.run()
