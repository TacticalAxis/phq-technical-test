# main.py
import os
import securescaffold
from flask import render_template, send_from_directory

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
