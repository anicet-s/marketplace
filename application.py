from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
import os
import json
import requests
from authlib.integrations.flask_client import OAuth
import logging
from jose import jwt

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

application = app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/catalogmenuwithusers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Configure OAuth with Authlib
oauth = OAuth(app)
oauth.register(
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
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))


# Item model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    category = db.Column(db.String(50))


# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'google_login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('home.html')
    return render_template('login.html')


@app.route('/furniture')
@login_required
def furniture():
    items = Item.query.filter_by(category='furniture').all()
    return render_template('furniture.html', items=items)


@app.route('/login')
def google_login():
    # Initialize OAuth flow with Google
    # Redirect to Google's authentication page
    session['nonce'] = os.urandom(16).hex()
    return oauth.google.authorize_redirect(redirect_uri=url_for('callback', _external=True), nonce=session['nonce'])


@app.route('/callback')
def callback():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token, nonce=session['nonce'])
    session["user_info"] = user_info
    return render_template('home.html')


@app.route('/cars')
@login_required
def cars():
    items = Item.query.filter_by(category='cars').all()
    return render_template('cars.html', items=items)


@app.route('/houses')
@login_required
def houses():
    items = Item.query.filter_by(category='houses').all()
    return render_template('houses.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)
