# main.py
import os
import securescaffold

from flask import render_template, send_from_directory, session
from authlib.integrations.flask_client import OAuth
from google.cloud import ndb
from app.auth import create_auth_blueprint, register_google_oauth
from app.models import GhostUser
from app.util import get_session_user, session_active

# flask app setup
app = securescaffold.create_app(__name__)

# init oauth
oauth = OAuth(app)
google_oauth = register_google_oauth(oauth)

# init ndb client
ndb_client = ndb.Client()

# create auth blueprint from factory
auth_bp = create_auth_blueprint(google_oauth, ndb_client)
app.register_blueprint(auth_bp)

@app.route("/")
def root():
    if session_active(session=session):
        user = get_session_user(session=session)
        ghost_users = []
        with ndb_client.context():
            ghost_user = GhostUser.get_by_id(user.get('sub'))
            ghost_users = GhostUser.query().filter(GhostUser.ghost_name != None).fetch() # type: ignore
            return render_template(
                "pages/index.html", user=user, ghost_users=ghost_users, ghost_user=ghost_user
            )
    else:
        return render_template(
            "pages/index.html", user=None
        )

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )
