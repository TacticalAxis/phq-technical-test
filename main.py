# main.py
import os
import securescaffold
from flask import render_template, send_from_directory
from securescaffold.contrib.appengine import users

app = securescaffold.create_app(__name__)

@app.route("/")
def root():
    return render_template(
        "pages/index.html", some_injected_value="piv_test", authenticated=False
    )


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/test")
def testauth():
    user = users.get_current_user()

    if user:
        email = user.email()
        user_id = user.user_id()

        return f"Hello signed-in user {email} {user_id}"
    
    return "Not signed-in"