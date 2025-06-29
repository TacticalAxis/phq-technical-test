import secrets

from flask import Blueprint
from flask import session, url_for, redirect

from authlib.integrations.flask_client import OAuth
from authlib.integrations.flask_client.apps import FlaskOAuth2App
from google.cloud import ndb
from google.cloud.ndb import Client

from app.models import GhostUser
from app.util import get_secret_value

def register_google_oauth(oauth: OAuth) -> FlaskOAuth2App:
    """Registers the OAuth2 client

    Args:
        oauth (OAuth): The OAuth2 Flask client.

    Returns:
        FlaskOAuth2App: Returns an instance of the The OAuth2 Flask client.
    """
    google = oauth.register(
        name='google',
        client_id=get_secret_value("GOOGLE_OAUTH2_CLIENT_ID"),
        client_secret=get_secret_value("GOOGLE_OAUTH2_CLIENT_SECRET"),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
    )
    
    return google # type: ignore

def create_auth_blueprint(oauth: FlaskOAuth2App, ndb_client: Client) -> Blueprint:
    """Creates the Auth blueprint for the /auth endpoint

    Args:
        oauth (FlaskOAuth2App): The registered OAuth2 Flask client.

    Returns:
        Blueprint: Returns a flask blueprint for the login, callback. and logout endpoints.
    """
    auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')
    
    @auth_blueprint.route('/login')
    def login():
        # Generate a nonce and store it in the session
        nonce = secrets.token_urlsafe(16)
        session['nonce'] = nonce
        redirect_uri = url_for('auth.callback', _external=True)
        return oauth.authorize_redirect(redirect_uri, nonce=nonce)

    @auth_blueprint.route('/callback')
    def callback():
        # Retrieve the nonce from the session
        nonce = session.get('nonce')
        token = oauth.authorize_access_token()
        user = oauth.parse_id_token(token, nonce=nonce)
        if user:
            session['user'] = user
            create_user_entry(
                ndb_client=ndb_client, 
                user_id=str(user.get('sub')),
                email=str(user.get('email'))
            )
        else:
            session.clear()
        return redirect(url_for('root'))

    @auth_blueprint.route('/logout')
    def logout():
        session.pop('user', None)
        session.pop('nonce', None)
        return redirect(url_for('root'))
    
    return auth_blueprint

def create_user_entry(ndb_client: Client, user_id: str, email: str) -> GhostUser:
    if not user_id:
        raise Exception("No user id specified!")
    if not email:
        raise Exception("No email specified!")
    
    with ndb_client.context():
        key = ndb.Key(GhostUser, user_id)

        # Check if a user with this user_id already exists
        existing_user = key.get()
        if existing_user:
            # Update email if it is different
            if existing_user.email != email:
                existing_user.email = email
                existing_user.put()  # Commit the update
            
            return existing_user

        # create a new used
        new_user = GhostUser(key=key, ghost_name=None, email=email)

        # commit
        new_user.put()
        
        return new_user