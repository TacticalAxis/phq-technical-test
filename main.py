# main.py
import os
import securescaffold

from flask import render_template, send_from_directory, session
from authlib.integrations.flask_client import OAuth
from google.cloud import ndb
from app.auth import create_auth_blueprint, register_google_oauth

# flask app setup
app = securescaffold.create_app(__name__)

# init oauth
oauth = OAuth(app)
google_oauth = register_google_oauth(oauth)

# init ndb client
ndb_client = ndb.Client()

# create auth blueprint from factory
auth_bp = create_auth_blueprint(google_oauth)
app.register_blueprint(auth_bp)

@app.route("/")
def root():
    user = session.get("user")
    return render_template(
        "pages/index.html", user=user
    )

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )
