# main.py
import os
import securescaffold

from flask import render_template, send_from_directory, session, redirect, url_for, request
from authlib.integrations.flask_client import OAuth
from google.cloud import ndb
from app.auth import create_auth_blueprint, register_google_oauth
from app.models import GhostUser
from app.util import get_session_user, load_ghost_names, pick_random_string, session_active

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

# load ghost names (from csv)
GHOST_NAMES = load_ghost_names()


@app.route("/")
def root():
    if session_active(session=session):
        user = get_session_user(session=session)
        ghost_users = []
        with ndb_client.context():
            # get the current ghost and the other ghosts (this could be more efficient)
            ghost_user = GhostUser.get_by_id(user.get('sub'))
            ghost_users = GhostUser.query().filter(GhostUser.ghost_name != None).fetch() # type: ignore
            return render_template(
                "pages/index.html", 
                user=user, 
                ghost_users=ghost_users, 
                ghost_user=ghost_user
            )
    else:
        return render_template(
            "pages/index.html", user=None
        )


@app.route("/picker")
def picker():
    if session_active(session=session):
        user = get_session_user(session=session)
        with ndb_client.context():
            # get the current ghost and the other ghosts (this could be more efficient)
            ghost_user:GhostUser = GhostUser.get_by_id(user.get('sub')) # type: ignore
            ghost_users = GhostUser.query().filter(GhostUser.ghost_name != None).fetch() # type: ignore
            taken_names = [g.ghost_name for g in ghost_users]
            remaining = pick_random_string(list_of_strings=[x.ghost_name for x in GHOST_NAMES], exclusions=taken_names)
            return render_template(
                "pages/picker.html",
                first_name=ghost_user.first_name,
                last_name=ghost_user.last_name,
                random_names=remaining
            )
    else:
        return redirect(url_for('root'))


@app.route('/submit', methods=['POST'])
def submit_name():
    if session_active(session=session):
        user = get_session_user(session=session)
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        ghost_name = request.form.get('ghost_name')
        
        # set the new attributes to the db model & commit
        with ndb_client.context():
            ghost_user:GhostUser = GhostUser.get_by_id(user.get('sub')) # type: ignore
            ghost_user.first_name = first_name
            ghost_user.last_name = last_name
            ghost_user.ghost_name = ghost_name
            ghost_user.put()
                
    return redirect(url_for('root'))


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )
