import secrets

from flask import Blueprint
from flask import session, url_for, redirect

from authlib.integrations.flask_client import OAuth
from authlib.integrations.flask_client.apps import FlaskOAuth2App

from util import get_secret_value

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

def create_auth_blueprint(oauth: FlaskOAuth2App) -> Blueprint:
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
        print("YESYESYES", url_for('auth.callback', _external=True))
        redirect_uri = url_for('auth.callback', _external=True)
        return oauth.authorize_redirect(redirect_uri, nonce=nonce)

    @auth_blueprint.route('/callback')
    def callback():
        # Retrieve the nonce from the session
        nonce = session.get('nonce')
        token = oauth.authorize_access_token()
        user = oauth.parse_id_token(token, nonce=nonce)
        session['user'] = user
        return redirect(url_for('root'))

    @auth_blueprint.route('/logout')
    def logout():
        session.pop('user', None)
        session.pop('nonce', None)
        return redirect(url_for('root'))
    
    return auth_blueprint
